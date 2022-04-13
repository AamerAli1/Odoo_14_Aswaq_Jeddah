odoo.define('custom_module.Screen', function (require) {
    "use strict";

    var PaymentScreen = require('point_of_sale.PaymentScreen')
    const { useListener } = require('web.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const Registries = require('point_of_sale.Registries');
    const TicketScreen = require('point_of_sale.TicketScreen');

    var models = require('point_of_sale.models');
    models.load_fields('pos.order', ['sltech_global_name']);
    models.load_fields('res.company', ['street']);

    var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                return Promise.resolve([]);
            }

            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 30000 * orders.length;

            // Keep the order ids that are about to be sent to the
            // backend. In between create_from_ui and the success callback
            // new orders may have been added to it.
            var order_ids_to_sync = _.pluck(orders, 'id');

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var args = [_.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                })];
            args.push(options.draft || false);
            return this.rpc({
                    model: 'pos.order',
                    method: 'create_from_ui',
                    args: args,
                    kwargs: {context: this.session.user_context},
                }, {
                    timeout: timeout,
                    shadow: !options.to_invoice
                })
                .then(function (server_ids) {
                    self.get_order().sltech_global_name = server_ids[0].sltech_global_name;
                    _.each(order_ids_to_sync, function (order_id) {
                        self.db.remove_order(order_id);
                    });
                    self.set('failed',false);
                    return server_ids;
                }).catch(function (reason){
                    var error = reason.message;
                    console.warn('Failed to send orders:', orders);
                    if(error.code === 200 ){    // Business Logic Error, not a connection problem
                        // Hide error if already shown before ...
                        if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                            self.set('failed',error);
                            throw error;
                        }
                    }
                    throw error;
                });
        },
	});

    const PaymentScreenInherit = (PaymentScreen) =>
        class extends PaymentScreen {
            async _finalizeValidation() {
                if ((this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) && this.env.pos.config.iface_cashdrawer) {
                    this.env.pos.proxy.printer.open_cashbox();
                }

                this.currentOrder.initialize_validation_date();
                this.currentOrder.finalized = true;

                let syncedOrderBackendIds = [];

    //            try {
                    if (this.currentOrder.is_to_invoice()) {
                        syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                            this.currentOrder
                        );
                    } else {
                        syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                    }
    //            } catch (error) {
    //                if (error.code == 700)
    //                    this.error = true;
    //                if (error instanceof Error) {
    //                    throw error;
    //                } else {
    //                    await this._handlePushOrderError(error);
    //                }
    //            }
                if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                    const result = await this._postPushOrderResolve(
                        this.currentOrder,
                        syncedOrderBackendIds
                    );
                    if (!result) {
                        await this.showPopup('ErrorPopup', {
                            title: 'Error: no internet connection.',
                            body: error,
                        });
                    }
                }

                this.showScreen(this.nextScreen);

                // If we succeeded in syncing the current order, and
                // there are still other orders that are left unsynced,
                // we ask the user if he is willing to wait and sync them.
                if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Remaining unsynced orders'),
                        body: this.env._t(
                            'There are unsynced orders. Do you want to sync these orders?'
                        ),
                    });
                    if (confirmed) {
                        // NOTE: Not yet sure if this should be awaited or not.
                        // If awaited, some operations like changing screen
                        // might not work.
                        this.env.pos.push_orders();
                    }
                }
            }
        }



    const TicketScreenInherit = (TicketScreen) =>
        class extends TicketScreen {
            async globalOrderNumber(id) {
                var global_order_number = "";
                await this.rpc({
                    model: "pos.order",
                    method: "search_read",
                    args: [[['pos_reference', '=', id]]],
                    fields: ['sltech_global_name'],
                }).then(function (output) {
                    if (output.length > 0)
                        global_order_number = output[0]['sltech_global_name']
                    return global_order_number
                });
                return await global_order_number;
            }
        }

    Registries.Component.extend(PaymentScreen, PaymentScreenInherit);
    Registries.Component.extend(TicketScreen, TicketScreenInherit);
    return PaymentScreen;


});
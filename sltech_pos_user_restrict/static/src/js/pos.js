odoo.define('sltech_pos_user_restrict.pos', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        compute_sa_qr_code(name, vat, date_isostring, amount_total, amount_tax) {
            /* Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
            https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
            */
            const seller_name_enc = this._compute_qr_code_field(1, name);
            const company_vat_enc = this._compute_qr_code_field(2, vat);
            //  ODOO THING 1 line
            // const timestamp_enc = this._compute_qr_code_field(3, date_isostring);
//            END
            // By SACHIN BURNAWAL
            var date = moment().format("YYYY-MM-DD hh:mm:ss.ms");
//            result.date.isostring = date.toLocaleString();
            const timestamp_enc = this._compute_qr_code_field(3, date);
            // END

            const invoice_total_enc = this._compute_qr_code_field(4, amount_total.toString());
            const total_vat_enc = this._compute_qr_code_field(5, amount_tax.toString());

            const str_to_encode = seller_name_enc.concat(company_vat_enc, timestamp_enc, invoice_total_enc, total_vat_enc);

            let binary = '';
            for (let i = 0; i < str_to_encode.length; i++) {
                binary += String.fromCharCode(str_to_encode[i]);
            }
            return btoa(binary);
        },
    });

});
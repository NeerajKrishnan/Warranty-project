odoo.define('pos_discount_limit.pos_discount_limit', function(require) {
    'use strict';

    const NumberPopup = require('point_of_sale.NumberPopup');
    const Registries = require('point_of_sale.Registries');





    const PosFrNumberPopup = NumberPopup => class extends NumberPopup {


   confirm(event) {
            var order    = this.env.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);

            var total = 0

          for (var i in lines) {



          if (lines[i].price>0)
          {
          total = total + lines[i].quantity*lines[i].price
          }}
          var discount = this.getPayload()
          discount = discount*total/100
          var discount_limit = this.env.pos.config.discount_limit
          if (discount <= discount_limit)
          {
          super.confirm(event)
          }
          else{
                 this.showPopup('DiscountLimitPopup', {
                            title: 'Discount Limit should be below  '+
                            discount_limit +" "+
                            this.env.pos.company_currency.symbol

                        });






      }



            }


    };

    Registries.Component.extend(NumberPopup, PosFrNumberPopup);

    return PosFrNumberPopup;
 });
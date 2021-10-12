odoo.define('pos_discount_limit.DiscountLimitPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');


    class DiscountLimitPopup extends AbstractAwaitablePopup {

        }

    DiscountLimitPopup.template = 'DiscountLimitPopup';


    Registries.Component.add(DiscountLimitPopup);

    return DiscountLimitPopup;
});
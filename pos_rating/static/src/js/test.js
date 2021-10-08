odoo.define('product_rating.product_rating', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    console.log('model',models)
    models.load_fields('product.product','product_rating');
    var _super_product = models.Product.prototype
    models.Product = models.Product.extend({
    initialize: function(attr,options) {

     var line =_super_product.initialize.apply(this, arguments);
     console.log(this.display_name)
     console.log(this.product_rating)

  }



  });



    var _super_orderline = models.Orderline.prototype
    models.Orderline = models.Orderline.extend({
    initialize: function(attr,options) {

     var line =_super_orderline.initialize.apply(this, arguments);

  },
export_for_printing: function () {
        var result = _super_orderline.export_for_printing.apply(this, arguments);
        result.product_rating = this.get_product().product_rating;
        return result;
    },



  });



});


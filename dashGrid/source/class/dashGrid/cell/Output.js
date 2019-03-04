qx.Class.define("dashGrid.cell.Output", {
  extend: qx.ui.core.Widget,

  construct: function(cellData) {
    this.base(arguments);

    this.setHandler(cellData);
  },

  properties: {
    handler: {
      check: "dashGrid.cell.Handler",
      nullable: false
    }
  },

  members: {

    getTitle: function() {
      return this.getHandler().getTitle();
    },

    getOutput: function() {
      return this.getHandler().getOutput();
    }
  }
});

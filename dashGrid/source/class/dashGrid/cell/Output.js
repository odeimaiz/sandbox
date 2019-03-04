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
    },

    getHtmlContent2: function() {
      let html = this.__title.getValue();
      html += this.getHandler().getOutput();
      return html;
    },

    setOutputContent: function(content) {
      if (this._getChildren().length > 1) {
        this._removeAt(1);
      }
      this._addAt(content, 1, {
        flex: 1
      });
    }
  }
});

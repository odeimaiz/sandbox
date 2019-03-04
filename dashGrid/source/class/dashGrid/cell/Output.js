qx.Class.define("dashGrid.cell.Output", {
  extend: qx.ui.core.Widget,

  construct: function(cellData) {
    this.base(arguments);

    this.setHandler(cellData);

    this._setLayout(new qx.ui.layout.VBox(10));

    let title = this.__title = this._createChildControlImpl("title");
    cellData.bind("title", title, "value");
    this._addAt(title, 0);
  },

  properties: {
    handler: {
      check: "dashGrid.cell.Handler",
      nullable: false
    }
  },

  events: {
    "backToGrid": "qx.event.type.Event"
  },

  members: {
    _createChildControlImpl: function(id) {
      let control;
      switch (id) {
        case "title": {
          control = new qx.ui.basic.Label();
          break;
        }
      }

      return control || this.base(arguments, id);
    },

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

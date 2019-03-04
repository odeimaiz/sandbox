qx.Class.define("dashGrid.widget.Dashboard", {
  extend: qx.ui.core.Widget,

  construct: function() {
    this.base(arguments);

    this._setLayout(new qx.ui.layout.Canvas());

    this.__outputs = {};

    this.init();
  },

  events: {
    "widgetSelected": "qx.event.type.Data"
  },

  members: {
    __gridterWr: null,
    __outputs: null,

    init: function() {
      let gridster = this.__gridterWr = new dashGrid.wrapper.Gridster();
      gridster.addListener("widgetSelected", e => {
        this.fireDataEvent("widgetSelected", e.getData());
      }, this);
      this._add(gridster, {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0
      })
    },

    addWidget: function(cellHandler) {
      let cellOutput = new dashGrid.cell.Output(cellHandler);
      let htmlElement = this.__gridterWr.addWidget(cellOutput);
      if (htmlElement) {
        this.__outputs[cellHandler.getUuid()] = htmlElement;
        cellHandler.addListener("changeTitle", e => {
          this.__gridterWr.rebuildWidget(cellOutput, htmlElement);
        }, this);
      }
    }
  }
});

/* global gridster */

/**
 * @asset(gridsterjs/*)
 */

qx.Class.define("dashGrid.wrapper.Gridster", {
  extend: qx.ui.core.Widget,

  statics: {
    NAME: "gridster",
    VERSION: "0.7.0",
    URL: "https://github.com/dsmorse/gridster.js"
  },

  construct: function() {
    this.base(arguments);
    this.set({
      width: 1000
    });
    this.init();
  },

  properties: {
    libReady: {
      nullable: false,
      init: false,
      check: "Boolean"
    },

    cellWidth: {
      nullable: false,
      init: 50,
      check: "Number"
    },

    cellHeight: {
      nullable: false,
      init: 50,
      check: "Number"
    }
  },

  events: {
    "widgetSelected": "qx.event.type.Data"
  },

  members: {
    __gridster: null,

    init: function() {
      // initialize the script loading
      const jQueryPath = "gridsterjs/jquery-3.3.1.min.js";
      const extras = false;
      const gridsterPath = extras ? "gridsterjs/jquery.gridster.with-extras-0.7.0.min.js" : "gridsterjs/jquery.gridster-0.7.0.min.js";
      const gridsterCss = "gridsterjs/jquery.gridster-0.7.0.min.css";
      const gridsterDemoCss = "gridsterjs/jquery.gridster.demo.css";
      const gridsterOsparcCss = "gridsterjs/jquery.gridster.osparc.css";
      const gridsterCssUri = qx.util.ResourceManager.getInstance().toUri(gridsterCss);
      const gridsterDemoCssUri = qx.util.ResourceManager.getInstance().toUri(gridsterDemoCss);
      const gridsterOsparcCssUri = qx.util.ResourceManager.getInstance().toUri(gridsterOsparcCss);
      qx.module.Css.includeStylesheet(gridsterCssUri);
      qx.module.Css.includeStylesheet(gridsterDemoCssUri);
      qx.module.Css.includeStylesheet(gridsterOsparcCssUri);
      let dynLoader = new qx.util.DynamicScriptLoader([
        jQueryPath,
        gridsterPath
      ]);

      dynLoader.addListenerOnce("ready", e => {
        console.log(gridsterPath + " loaded");
        this.setLibReady(true);
        this.__createEmptyLayout();
        // this.__fillWDummy();
      }, this);

      dynLoader.addListener("failed", e => {
        let data = e.getData();
        console.error("failed to load " + data.script);
      }, this);

      dynLoader.start();
    },

    __createEmptyLayout: function() {
      let gridsterPlaceholder = qx.dom.Element.create("div");
      qx.bom.element.Attribute.set(gridsterPlaceholder, "id", "gridster");
      qx.bom.element.Attribute.set(gridsterPlaceholder, "class", "gridster");
      qx.bom.element.Style.set(gridsterPlaceholder, "width", "100%");
      qx.bom.element.Style.set(gridsterPlaceholder, "height", "100%");
      this.getContentElement().getDomElement()
        .appendChild(gridsterPlaceholder);

      let cellsList = qx.dom.Element.create("ul");
      gridsterPlaceholder.appendChild(cellsList);

      this.__gridster = $(".gridster ul").gridster({
        "widget_base_dimensions": [this.getCellWidth(), this.getCellHeight()],
        "widget_margins": [5, 5],
        "max_cols": 20,
        // "helper": "clone",
        "resize": {
          "enabled": true,
          "max_size": [500, 500]
        },
        "draggable": {
          "handle": "header"
        }
      }).data('gridster');
    },

    createCellOptions: function(dataCol = 1, dataRow = 1, dataSizeX = 1, dataSizeY = 1) {
      return {
        "row": dataRow,
        "col": dataCol,
        "sizex": dataSizeX,
        "sizey": dataSizeY
      };
    },

    __buildHeader: function(cellOutput) {
      let html = "<header>";
      html += cellOutput.getTitle();
      html += "</header>";
      return html;
    },

    __buildContent: function(cellOutput) {
      let html = cellOutput.getOutput();
      return html;
    },

    __buildHtmlCode: function(cellOutput) {
      let html = "<li>";
      html += this.__buildHeader(cellOutput);
      html += this.__buildContent(cellOutput);
      html += "</li>";
      return html;
    },

    addWidget2: function(cellOutput) {
      const html = this.__buildHtmlCode(cellOutput);
      let jQueryElement = this.__gridster.add_widget(html, 8, 6);
      if (jQueryElement) {
        let htmlElement = jQueryElement.get(0);
        htmlElement.addEventListener("dblclick", e => {
          this.fireDataEvent("widgetSelected", cellOutput.getHandler().getUuid());
        }, this);
      }
    },

    addWidget: function(html, sizex, sizey, col, row) {
      // let cellOutput = new dashGrid.cell.Output();
      // cellOutput.setOutputContent(html);
      html = "<li>" + html + "</li>";
      const jQueryElement = this.__gridster.add_widget(html, sizex, sizey, col, row);
      const htmlElement = jQueryElement.get(0);
      htmlElement.addEventListener("dblclick", (e) => {
        this.fireDataEvent("widgetSelected", e.currentTarget);
      }, this)
    },

    __fillWDummy: function() {
      const init = [
        [1, 1, 4, 4],
        [6, 1, 2, 4],
        [8, 1, 2, 2],
        [4, 6, 6, 2],
        [1, 8, 2, 2],
        [1, 6, 2, 2],
        [4, 8, 2, 2],
        [4, 10, 2, 2]
      ];

      for (let i=0; i<init.length; i++) {
        const c = init[i];
        const options = this.createCellOptions(c[0], c[1], c[2], c[3]);
        this.addTextWidget(options);
      }
      this.addSVGWidget(10, 12);
    },

    addTextWidget: function(options) {
      const html = this.getRandomText();
      this.addWidget(html, options.sizex, options.sizey, options.col, options.row);
    },

    addSVGWidget: function(col, row) {
      const html = this.getSVGChart();
      this.addWidget(html, Math.ceil(800/this.getCellWidth()), Math.ceil(600/this.getCellHeight()), col, row);
    }
  }
});

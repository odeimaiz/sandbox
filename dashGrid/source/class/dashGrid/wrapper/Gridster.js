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

    this.__init();
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

  statics: {
    buildHeader: function(cellOutput) {
      let html = "<header>";
      html += cellOutput.getTitle();
      html += "</header>";
      return html;
    },

    buildContent: function(cellOutput) {
      let html = "<content>";
      html += cellOutput.getOutput();
      html += "</content>";
      return html;
    },

    buildHtmlCode: function(cellOutput) {
      let html = this.buildHeader(cellOutput);
      html += this.buildContent(cellOutput);
      return html;
    },

    buildHtmlCodeInList: function(cellOutput) {
      let html = "<li>";
      html += this.buildHtmlCode(cellOutput);
      html += "</li>";
      return html;
    },
  },

  members: {
    __gridster: null,

    __init: function() {
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

    addWidget: function(cellOutput) {
      const html = this.self().buildHtmlCodeInList(cellOutput);
      let jQueryElement = this.__gridster.add_widget(html, 8, 6);
      if (jQueryElement) {
        let htmlElement = jQueryElement.get(0);
        htmlElement.addEventListener("dblclick", e => {
          this.fireDataEvent("widgetSelected", cellOutput.getHandler().getUuid());
        }, this);
        return htmlElement;
      }
      return null;
    },

    rebuildWidget: function(cellOutput, htmlElement) {
      let html = this.self().buildHtmlCode(cellOutput);
      html += "<span class='gs-resize-handle gs-resize-handle-both'></span>";
      htmlElement.innerHTML = html;
    }
  }
});

/**
 * This is the main application class of "dashGrid"
 *
 * @asset(dashGrid/*)
 */

qx.Class.define("dashGrid.Application", {
  extend : qx.application.Standalone,

  members: {
    __stack: null,
    __mainView: null,
    __gridder: null,
    __cellEditors: null,
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    main: function() {
      // Call super class
      this.base(arguments);

      this.__cellEditors = {};

      let stack = this.__stack = new qx.ui.container.Stack();

      let mainView = this.__mainView = new qx.ui.container.Composite(new qx.ui.layout.VBox());
      let addBtn = this._createChildControlImpl("addBtn");
      mainView.add(addBtn);
      let gridder = this.__gridder = this._createChildControlImpl("gridder");
      mainView.add(gridder, {
        flex: 1
      });
      
      stack.add(mainView);

      // Document is the application root
      let doc = this.getRoot();

      // Add button to document at fixed coordinates
      doc.add(stack, {
        left: 0,
        top: 0,
        right: 0,
        bottom: 0
      });
    },

    _createChildControlImpl: function(uuid) {
      let control;
      switch (uuid) {
        case "addBtn": {
          control = new qx.ui.form.Button(this.tr("Add plot"));
          control.addListener("execute", e => {
            let cellHandler = new dashGrid.cell.Handler();
            let cellEditor = new dashGrid.cell.Editor(cellHandler);
            cellEditor.addListener("backToGrid", () => {
              this.__stack.setSelection([this.__mainView]);
            }, this);
            let cellOutput = new dashGrid.cell.Output(cellHandler);
            this.__cellEditors[cellHandler.getUuid()] = cellEditor;
            this.__gridder.addWidget(cellOutput);
          }, this);
          break;
        }
        case "gridder": {
          control = new dashGrid.wrapper.Gridster();

          control.addListener("widgetSelected", e => {
            const uuid = e.getData();
    
            let cellEditor = null;
            if (this.__cellEditors.hasOwnProperty(uuid)) {
              cellEditor = this.__cellEditors[uuid];
              // cellEditor.setHtmlContent(htmlContent);
              this.__stack.add(cellEditor);
              this.__stack.setSelection([cellEditor]);
            }
          }, this);
          break;
        }
      }

      return control || this.base(arguments, uuid);
    }
  }
});
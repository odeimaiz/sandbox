qx.Class.define("landing_docs.LandingPage", {
  extend: qx.ui.core.Widget,

  construct: function() {
    this.base(arguments);

    // Layout guarantees it gets centered in parent's page
    let layout = new qx.ui.layout.Grid();
    layout.setRowFlex(0, 1);
    layout.setColumnFlex(0, 1);
    this._setLayout(layout);

    let vBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(10));

    let icon = this.__createIcon();
    vBox.add(icon);
    
    vBox.add(new qx.ui.core.Spacer(0, 50));

    let lists = this.__createLists();
    vBox.add(lists, {
      flex: 1
    });

    this._add(vBox, {
      row:0,
      column:0
    });
  },

  members: {
    __createIcon: function() {
      let atm = new qx.ui.basic.Atom().set({
        icon: "landing_docs/osparc-white-docs.png",
        iconPosition: "top"
      });
      atm.getChildControl("icon").set({
        width: 250,
        height: 85,
        scale: true
      });
      return atm;
    },

    __createLists: function() {
      let hBox = new qx.ui.container.Composite(new qx.ui.layout.HBox(10));

      let reports = this.__createReportsList();
      hBox.add(reports, {
        flex: 1
      });

      let user = this.__createUserList();
      hBox.add(user, {
        flex: 1
      });

      let devel = this.__createDevelList();
      hBox.add(devel, {
        flex: 1
      });

      return hBox;
    },

    __createReportsList: function() {
      const entries = [
        ["Technical Specs. & Technology Evaluation [D1.1]", "https://osparc-docs.readthedocs.io/en/latest/"]
      ];
      return this.__createList("Reports", entries);
    },

    __createUserList: function() {
      const entries = [];
      return this.__createList("User", entries);
    },

    __createDevelList: function() {
      const entries = [
        ["Frontend API", qx.util.ResourceManager.getInstance().toUri("../devel/frontend/latest/apiviewer/index.html")]
      ];
      return this.__createList("Devel", entries);
    },

    __createList: function(label, entries) {
      let vBox = this.__createVBoxWLabel(label);

      entries.forEach(pair => {
        let entry = this.__createListEntry(pair[0], pair[1]);
        vBox.add(entry);
      }, this);

      return vBox;
    },

    __createVBoxWLabel: function(text) {
      let vBoxLayout = new qx.ui.container.Composite(new qx.ui.layout.VBox(10));

      let label = new qx.ui.basic.Label(text).set({
        font: qx.bom.Font.fromConfig(landing_docs.theme.Font.fonts["nav-bar-label"]),
        minWidth: 150
      });
      vBoxLayout.add(label);

      return vBoxLayout;
    },

    __createListEntry: function(text, link) {
      let txt = "<center><style='color: gray'>- " + text + "</center>";
      let atm = new qx.ui.basic.Atom(txt);
      let lbl = atm.getChildControl("label");
      lbl.setRich(true);
      lbl.setAllowGrowY(true);
      atm.addListener("mouseover", function() {
        atm.setLabel("<u style='color: gray'>" + txt + "</u>");
      }, this);
      atm.addListener("mouseout", function() {
        atm.setLabel(txt);
      }, this);
      atm.addListener("click", () => {
        window.open(link);
      });

      return atm;
    }
  }
});
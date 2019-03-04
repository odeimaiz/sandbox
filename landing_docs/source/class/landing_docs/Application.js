/**
 * This is the main application class of "landing_docs"
 *
 * @asset(landing_docs/*)
 */

qx.Class.define("landing_docs.Application",
{
  extend : qx.application.Standalone,



  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    main : function()
    {
      // Call super class
      this.base(arguments);
      
      let landingPage = new landing_docs.LandingPage();
      const options = {
        top: "10%",
        bottom: 0,
        left: "20%",
        right: "20%"
      };
      this.getRoot().add(landingPage, options);
    }
  }
});
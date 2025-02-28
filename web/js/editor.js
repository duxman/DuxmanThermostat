  function loadEditor( fichero, tab, jsondata, esarray )
  {
    JSONEditor.defaults.options.theme = 'bootstrap3';
    JSONEditor.defaults.options.iconlib = "fontawesome4";
    // Initialize the editor
    editor = new JSONEditor(document.getElementById(tab),
    {

        // Enable fetching schemas via ajax
        ajax: true,

        // The schema for the editor
        schema:
        {
            $ref: "/schemas/"+fichero
        },

        // Seed the form with a starting value
        //startval: starting_value,

        // Disable additional properties
        no_additional_properties: true,
        disable_edit_json : !esarray,
        disable_collapse : true,
        disable_array_add : !esarray,
        disable_array_delete : !esarray,
        disable_properties : true,

        // Require all properties by default
        required_by_default: true,

        // Seed the form with a starting value
        startval: jsondata
    });

    // Listen for changes
    editor.on("change",  function()
    {
        // Do something...
    });

    return editor;
  }

  function loadEditorDefault( fichero, tab, esarray )
  {
    JSONEditor.defaults.options.theme = 'bootstrap3';
    JSONEditor.defaults.options.iconlib = "fontawesome4";
    // Initialize the editor
    editor = new JSONEditor(document.getElementById(tab),
    {

        // Enable fetching schemas via ajax
        ajax: true,

        // The schema for the editor
        schema:
        {
            $ref: "/schemas/"+fichero
        },

        // Seed the form with a starting value
        //startval: starting_value,

        // Disable additional properties
        no_additional_properties: true,
        disable_edit_json : !esarray,
        disable_collapse : true,
        disable_array_add : !esarray,
        disable_array_delete : !esarray,
        disable_properties : true,

        // Require all properties by default
        required_by_default: true,
    });

    // Listen for changes
    editor.on("change",  function()
    {
        // Do something...
    });

    return editor;
  }

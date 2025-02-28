function openTab(evt, tab)
{
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++)
    {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++)
    {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tab).style.display = "block";
    evt.currentTarget.className += " active";
}

function CreateEvents()
{
    document.getElementById('submitProgramacion').addEventListener('click',function()
        {
            var datos = editorProgramacion.getValue()
            $.ajax
            (
              {
                type: "POST",
                url: "/cgi/store.py",
                data: { type : "PROGRAMACION"  ,filename: "programacion.json" , contenido: JSON.stringify(datos)},
                dataType: "text"
              }
            ).done(function( o ) { alert("OK PROGRAMACION GRABADA"); });
            // Get the value from the editor
            console.log(datos);
        });

        document.getElementById('submitPrograms').addEventListener('click',function()
        {
            var datos = editorProgramas.getValue()
            $.ajax
            (
              {
                type: "POST",
                url: "/cgi/store.py",
                data: { type : "PROGRAMS"  ,filename: "ProgramConfiguration.json" , contenido: JSON.stringify(datos)},
                dataType: "text"
              }
            ).done(function( o )
            {
                alert("OK PROGRAMS SAVED");
            });
            // Get the value from the editor
            console.log(datos);
        });

         document.getElementById('submitZones').addEventListener('click',function()
        {
            var datos = editorZonas.getValue()
            $.ajax
            (
              {
                type: "POST",
                url: "/cgi/store.py",
                data: { type : "ZONES"  ,filename: "Zones.json" , contenido: JSON.stringify(datos)},
                dataType: "text"
              }
            ).done(function( o )
            {
                alert("OK ZONES SAVED");
            });
            // Get the value from the editor
            console.log(datos);
        });


        document.getElementById('submitGeneral').addEventListener('click',function()
        {
            var datos = editorGeneral.getValue()
            var useExternalServer = ( editorGeneral.editors["root.WebServerType"].value != "INTERNAL");

            if ( useExternalServer )
                $.post('/cgi/store.php',  { "type" : "GENERAL" , "filename": "../config/configuracion.json" , "contenido": JSON.stringify(datos)}).done(function(datos) {alert("OK Configuration saved with PHP"); } );
            else
                $.ajax
                (
                  {
                    type: "POST",
                    url: "/cgi/store.py",
                    data: { type : "GENERAL" , filename: "configuracion.json" , contenido: JSON.stringify(datos)},
                    dataType: "text"
                  }
                ).done(function( o ) { alert("OK CONFIGURACION GRABADA"); });
            // Get the value from the editor
            console.log(datos);
        });

        document.getElementById('submitI2C').addEventListener('click',function()
        {
            var datos = editorI2C.getValue()
            $.ajax
            (
              {
                type: "POST",
                url: "/cgi/store.py",
                data: { type : "I2C" , filename: "I2CConfig.json" , contenido: JSON.stringify(datos)},
                dataType: "text"
              }
            ).done(function( o ) { alert("OK CONFIGURACION I2C GUARDADA"); });
            // Get the value from the editor
            console.log(datos);
        });
}
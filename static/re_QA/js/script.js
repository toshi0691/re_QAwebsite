window.addEventListener("load" , function (){ 

    var config_date = { 
        "locale": "ja"
    }   
    var config_time = { 
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        "locale": "ja"
    }   
    var config_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        "locale": "ja"
    }   


    flatpickr("#date", config_date);
    flatpickr("#time", config_time);

    var config_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        "locale": "ja"
    }

    flatpickr("#dt",config_dt)

});
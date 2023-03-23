document.addEventListener('DOMContentLoaded', function (event) {
    var baseHost = document.location.origin
    var streamUrl = baseHost + ':81'

    const hide = el => {
        el.classList.add('hidden')
    }
    const show = el => {
        el.classList.remove('hidden')
    }

    const disable = el => {
        el.classList.add('disabled')
        el.disabled = true
    }

    const enable = el => {
        el.classList.remove('disabled')
        el.disabled = false
    }

    const updateValue = (el, value, updateRemote) => {
        updateRemote = updateRemote == null ? true : updateRemote
        let initialValue
        if (el.type === 'checkbox') {
        initialValue = el.checked
        value = !!value
        el.checked = value
        } else {
        initialValue = el.value
        el.value = value
        }

        if (updateRemote && initialValue !== value) {
        updateConfig(el);
        } else if(!updateRemote){
        if(el.id === "aec"){
            value ? hide(exposure) : show(exposure)
        } else if(el.id === "agc"){
            if (value) {
            show(gainCeiling)
            hide(agcGain)
            } else {
            hide(gainCeiling)
            show(agcGain)
            }
        } else if(el.id === "awb_gain"){
            value ? show(wb) : hide(wb)
        } else if(el.id === "face_recognize"){
            value ? enable(enrollButton) : disable(enrollButton)
        }
        }
    }



    function updateConfig (el) {
        let value
        switch (el.type) {
        case 'checkbox':
            value = el.checked ? 1 : 0
            break
        case 'range':
        case 'select-one':
            value = el.value
            break
        case 'button': //AGREGAR CONDICIONALES MOTOR
        case 'submit':
            value = '1'
            console.log(`Boton presionado`)
            break
        default:
            return
        }

        const query = `${baseHost}/control?var=${el.id}&val=${value}`

        fetch(query)
        .then(response => {
            console.log(`request to ${query} finished, status: ${response.status}`)
        })
    } 
    
    function updateMotor(status, value){
        const motorQuery = `${baseHost}/motor?var=${status.id}&val=${value}`
        fetch(motorQuery)
        .then(response => {
            console.log(`request to ${motorQuery} finished, status: ${response.status}`)
        })
    }
 

    document
        .querySelectorAll('.close')
        .forEach(el => {
        el.onclick = () => {
            hide(el.parentNode)
        }
        })




    // Attach default on change action
    document
        .querySelectorAll('.default-action')
        .forEach(el => {
        el.onchange = () => updateConfig(el)
        })

    const framesize = "3"

    framesize.onchange = () => {
        updateConfig(framesize)
    }

    class ClickAndHold {
        /**
         * 
         * @param {EventTarget} target the HTML element to apply the event to
         * @param {Function} callback  The function to run once the target is clicked and held
         */

        constructor(target, callback){
            this.target = target;
            this.callback = callback;
            this.isHeld = false;
            this.activeHoldTimeoutId = null; 

            ["mousedown", "touchstart"].forEach(type =>{
                this.target.addEventListener(type, this._onHoldStart.bind(this));
            });

            ["mouseup","mouseleave", "mouseout"].forEach(type => {
                this.target.addEventListener(type, this._onHoldEnd.bind(this));
            });


        }

        _onHoldStart() {
            this.isHeld = true;
                    this.activeHoldTimeoutId = setTimeout(() => {if (this.isHeld){
                    this.callback(this.target, "1"); 
                }
        },1000 )
            
        }

        _onHoldEnd() {
            this.isHeld = false;
            this.callback(this.target,"0");
            clearTimeout(this.activeHoldTimeoutId);
        }


        static apply (target, callback){
            new ClickAndHold (target, callback)
        }
    }

    const upButton =  document.getElementById("up_button");
    const leftButton =  document.getElementById("left_button");
    const downButton =  document.getElementById("down_button");
    const rigthButton =  document.getElementById("right_button");
    ClickAndHold.apply(upButton, updateMotor)
    ClickAndHold.apply(leftButton, updateMotor)
    ClickAndHold.apply(downButton, updateMotor)
    ClickAndHold.apply(rigthButton, updateMotor)


    const motorSpeed = document.getElementById("speed");
    motorSpeed.onchange = () =>{updateMotor(motorSpeed.id, motorSpeed.value)};


    var messageForm = document.getElementById("tts-form");

    messageForm.addEventListener ('submit',function(event){
        event.preventDefault()
        var messageTts = document.getElementById('message').value;

        const messageQuery = `${baseHost}/message?var=${'tts'}&val=${messageTts}`
        fetch(messageQuery)
        .then(response => {
            console.log(`request to ${messageQuery} finished, status: ${response.status}`)
        })                
        
    })

})
var token = '{{csrf_token}}';

document.addEventListener('DOMContentLoaded', () =>{
    document.querySelectorAll('.customize').forEach( button =>{
        button.onclick = () => {
            const request = new XMLHttpRequest();
            const info = button.id;

            request.open('POST', '/main_app/')
    
              request.onload = () => {
                const data = JSON.parse(request.responseText);
                var parent = document.querySelector("#form_contents");
                if(data.pizza){
                  name_select(parent, data.toppings_no, data.name , data.price, data.size, "not_req" );
                  if(data.toppings_no > 0 && data.toppings_no < 4){
                    let div = document.createElement("div");
                    div.id = "inner_info";
                    div.innerHTML= "Customize";
                    parent.appendChild(div);
                    for(let i = 0; i < data.toppings_no; i++){
                      let select_list = document.createElement("select");
                      select_list.class = "piz_sel_class";
                      select_list.id = `myselectpizza${i}`;
                      select_list.name = `pizzaselect${i}`;
                      select_list.style.margin = '5px';
                      parent.appendChild(select_list);

                      for(let j = 0; j < data.toppings.length; j++){
                        let option = document.createElement("option");
                        option.value = data.toppings[j];
                        option.text = data.toppings[j];
                        select_list.appendChild(option);
                      } 
                    }
                    document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                    showmodal('.bg_mymodal', '#enter','#cancel');
                  }else if(data.toppings_no > 3){
                    let div = document.createElement("div");
                    div.id = "inner_info";
                    div.innerHTML= "This pizza will have 5 surprise toppings";
                    parent.appendChild(div);
                    document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                    showmodal('.bg_mymodal', '#enter','#cancel')
                  }else{
                    let div = document.createElement("div");
                    div.id = "inner_info";
                    div.innerHTML= "No toppings Pizza";
                    parent.appendChild(div);
                    document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                    showmodal('.bg_mymodal', '#enter','#cancel');
                  }

                }else if(data.dinner){
                  name_select(parent, "no", data.name , data.price, data.size, 'dinner' );
                  document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                  showmodal('.bg_mymodal', '#enter','#cancel');
                }
                else if(data.salad){
                  name_select(parent, "no", data.name , data.price, "no", "salad" );
                  document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                  showmodal('.bg_mymodal', '#enter','#cancel');
                }
                else if(data.pasta){
                  name_select(parent, "no", data.name , data.price, "no", "pasta" );
                  document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                  showmodal('.bg_mymodal', '#enter','#cancel');
                }
                else if(data.sub){
                  let valtopass = [];
                  var real_price = parseFloat(data.price);
                  const br = document.createElement('br');
                  name_select(parent, data.toppings_no, data.name , data.price, data.size, "not_req" );
                  parent.appendChild(br);
                  for(let i=0; i < data.toppings_no; i++){
                    let newCheckBox = document.createElement('input');
                    const p = document.createElement('p');
                    const span_extra = document.createElement('span'); 
                    span_extra.innerHTML = data.toppings[i];
                    span_extra.style.position = "relative";
                    span_extra.style.top = "-5px"
                    span_extra.style.left = "-10px";
                    newCheckBox.name= `newCheckBox${i}`;
                    newCheckBox.type = 'checkbox';
                    newCheckBox.class = "checkboxes";
                    newCheckBox.id = `check${data.toppings[i]}`
                    newCheckBox.value = data.toppings[i];
                    newCheckBox.style.position = "absolute";
                    newCheckBox.style.left = "10px";
                    parent.innerHTML += newCheckBox.outerHTML + span_extra.outerHTML + br.outerHTML;
                  }
                  document.querySelector("#final_price").innerHTML = `Price: $${data.price}`;
                  showmodal('.bg_mymodal', '#enter','#cancel');
                  if(data.toppings_no === 1){
                    check_box(`check${data.toppings[0]}`,"newCheckBox0");
 
                  }else{
                    check_box(`check${data.toppings[0]}`,"newCheckBox0");
                    check_box(`check${data.toppings[1]}`,"newCheckBox1");
                    check_box(`check${data.toppings[2]}`,"newCheckBox2");
                    check_box(`check${data.toppings[3]}`,"newCheckBox3");

                    
                  }
                  
                  function check_box(chck_id, chck_name){
                    document.getElementById(chck_id).onclick = () =>{
                      document.getElementById(chck_id).disabled = true;
                      document.getElementById('enter').disabled = true;
                      document.getElementById('enter').value = "Wait..";
                      document.getElementById('cancel').disabled = true;
                      document.getElementById('cancel').innerHTML = "Wait..";
                      setTimeout(function(){
                        if(document.getElementById(chck_id).checked){
                          real_price = real_price + 0.50;
                          real_price = Number((real_price).toFixed(2));
                          document.querySelector("#final_price").innerHTML = `Price: $${real_price}`;
                          valtopass.push(chck_name);
                          document.getElementById('select_id').options[0].value = data.toppings_no + data.size + `${data.name})`  + valtopass + "#" + real_price;
                        }else{
                          real_price = real_price - 0.50;
                          real_price = Number((real_price).toFixed(2));
                          document.querySelector("#final_price").innerHTML = `Price: $${real_price}`;
                          if(valtopass.includes(chck_name)){
                            this_index = valtopass.indexOf(chck_name);
                            valtopass.splice(this_index,1);
                          }
                          document.getElementById('select_id').options[0].value = data.toppings_no + data.size + `${data.name})`  + valtopass + "#" + real_price;

                        }
                        document.getElementById(chck_id).disabled = false;
                        document.getElementById('enter').disabled = false;
                        document.getElementById('enter').value = "Add to cart";
                        document.getElementById('cancel').disabled = false;
                        document.getElementById('cancel').innerHTML = "Cancel";
                      },500);
                      
                  }
                  }
                }

            } 
          
            const data = new FormData();
            data.append('info', info);
    
            request.send(data);
            return false;
        }
    });



    function showmodal(modal_adr, submit_adr, cancel_adr){
      document.querySelector(modal_adr).style.display = 'flex';
     
      document.querySelector(submit_adr).onclick = () => {
        document.querySelector(modal_adr).style.display = 'none';   
     }
      document.querySelector(cancel_adr).onclick = () => {
        document.querySelector(modal_adr).style.display = 'none';
        document.querySelector('#form_contents').innerHTML = "";
      }
    }

    function name_select(parent_element, data_toppings_no, data_name, data_price, data_size,simple_name ){
      let select_name = document.createElement("select");
      select_name.id = 'select_id';
      select_name.name="select_name";
      select_name.style.marginBottom = '10px';
      parent_element.appendChild(select_name);
      let option_name = document.createElement("option");
      if(data_toppings_no != 'no'){        
        option_name.value= data_toppings_no + data_size + `${data_name})` +  data_price;
      }
      else if(data_toppings_no == "no"){       
        if(data_size != "no"){
          option_name.value = data_size + data_name + ` ${simple_name})` + data_price;
        }else if(data_size === "no"){
          option_name.value = data_name + `#${simple_name}` + data_price;
        }
        
      }
      if(data_size != "no"){
        option_name.text = `${data_name} (${data_size})`;
      }else if(data_size === "no"){
        option_name.text = data_name;
      }     
      select_name.appendChild(option_name);
    }

    document.querySelectorAll('.delete').forEach( button =>{
      button.onclick = () =>{
        const request = new XMLHttpRequest();
        const del_info = button.id
        request.open("POST", "/delete/")

        request.onload = () => {
          document.location.reload(true);
        }

        const data = new FormData();
        data.append('del_info', del_info);
        

        request.send(data);
        return false;

      }
    })


    document.querySelectorAll('.complete_order').forEach( button =>{
      button.onclick = () =>{
        const request = new XMLHttpRequest();
        const cmplt_info = button.id
        request.open("POST", "/owner_page/")

        request.onload = () => {
          document.location.reload(true);
        }

        const data = new FormData();
        data.append('cmplt_info', cmplt_info);
        

        request.send(data);
        return false;

      }
    })
    document.querySelectorAll('.delete_o_history').forEach( button =>{
      button.onclick = () =>{
        const request = new XMLHttpRequest();
        const o_del = button.id
        request.open("POST", "/delete/")

        request.onload = () => {
          document.location.reload(true);
        }

        const data = new FormData();
        data.append('o_del', o_del);
        

        request.send(data);
        return false;

      }
    })
});


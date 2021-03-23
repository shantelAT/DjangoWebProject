console.log('Hi How are ya!')
var updateBtns  = document.getElementsByClassName('update-cart')

for(var i = 0; i< updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:', productId, 'action:', action)

    console.log('USER:', user)
    if(user === 'AnonymousUser'){
      console.log('Not logded in')
    }else{
      updateUserOrder(productId, action)
    }

  })
}

function updateUserOrder(productId, action){
    console.log('User authenticated sending data...')

    var url = '/update_item/'

    fetch(url, {        //fect set to url
      method: 'POST',   // fetch type post
      headers:{
        'Content-Type': 'application/json',
        'X-CSRFtoken':csrftoken,      // TOKEN CALL
      },
      body: JSON.stringify({'productId':productId, 'action':action})      //data passed
    })
    .then((response) => {        //response intp json
      return response.json()
    })
    .then((data) => {
      console.log('data:', data)  //console response
      location.reload()
    })

}
/*
var OrderComplete  = document.getElementsByClassName('page')

for(var i = 0; i< OrderComplete.length; i++){
  OrderComplete[i].addEventListener('click', function(){
    document.getElementById('page').classList.add("hidden");
  })
}*/

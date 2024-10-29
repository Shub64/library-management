 // Function to change the iframe source based on the selected menu option  
 function changeIframeContent(page) {  
    const iframe = document.getElementById('contentIframe');  
    // Change the src of the iframe based on the selected value  
    iframe.src = page;  
}  

// Toggle menu visibility  
document.querySelector('.menu-toggle').addEventListener('click', function() {  
    document.getElementById('menu').classList.toggle('active');  
});
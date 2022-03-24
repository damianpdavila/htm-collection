<script>
    // LinkedIn event tracking
    jQuery(document).ready(function () {
    jQuery('.linkedin-event a').click(function(event) { 
        jQuery('body').append('<img src="https://howtomanageasmalllawfirm.com/wp-content/uploads/2019/05/Phone_Start-Menu.png" style="width: 50px; height: 50px; position: absolute; left:0; bottom: 0;">');  
        setTimeout(clickIt, 250, event.delegateTarget );
        jQuery('.linkedin-event a').off('click'); 
        return false;
    });
    var clickIt = function(elementToClick) {
        jQuery(elementToClick)[0].click();
    };
    });
</script>
<!--script src="https://howtomanage.activehosted.com/f/embed.php?id=166" type="text/javascript" charset="utf-8"></script-->
<!--button type="button" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#optinModal">Launch demo modal</button-->
<!-- Modal -->
<div class="modal fade" id="optinModal" tabindex="-1" role="dialog" aria-labelledby="optinModalLabel">
	<div class="vertical-alignment-helper">
		<div class="modal-dialog vertical-align-center" role="document">
			<div class="modal-content">
				<div class="modal-body">
					<p><img src="https://ac-image.s3.amazonaws.com/5/2/4/0/3/1/home/admin/htm-logo.png" class="img-responsive center-block" width="200" style="width: 200px; max-width: 100%;" />
					<h3 class="modal-title text-center" id="myModalLabel">Enter the Password to access your Business Plan Bootcamp Materials</h3>
					
					<form action="https://howtomanage.activehosted.com/proc.php" id="_form_166_" method="post">
						<input type="hidden" name="u" value="166" />
						<input type="hidden" name="f" value="166" />
						<input type="hidden" name="s" />
						<input type="hidden" name="c" value="0" />
						<input type="hidden" name="m" value="0" />
						<input type="hidden" name="act" value="sub" />
						<input type="hidden" name="v" value="2" />
						<input type="hidden" id="HiddenPassword" value="VIPappointment">
						<div class="form-group"><input type="text" name="firstname" placeholder="Your First Name" required/></div>
						<div class="form-group"><input class="form-control" type="email" name="email" id="email" placeholder="Your Email" /></div>
						<div class="form-group"><input class="form-control" type="password" name="field[16]" id="VIPPassword" placeholder="Enter the Password" /></div>
						<div class="text-center"><button type="submit" class="btn btn-success btn-lg">Let Me In!</button></div>
					</form>
				</div>
			</div>
		</div>
	</div>
</div>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.17.0/jquery.validate.js"></script>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<style>
.vertical-alignment-helper {
    display: table;
    height: 100%;
    width: 100%;
    pointer-events: none;
    position: relative;
    z-index: 1045;
}
.vertical-align-center {
    display: table-cell;
    vertical-align: middle;
    pointer-events: none;
}
.modal-content {
	width: inherit;
	max-width: inherit;
	height: inherit;
	margin: 0 auto;
	pointer-events: all;
}
.modal-backdrop, .modal-backdrop.in {
	background-color: rgba(0,0,0,1);
}
.modal-backdrop.in {
	filter: alpha(opacity=80);
	opacity: .8;
}
#av-layout-grid-1 {
	z-index: 9999;
	border: none !important;
}
#av-layout-grid-1 .container, #av-layout-grid-1 .content {
	padding: 0px !important;
	min-height: 0px !important;
}
#av-layout-grid-1 .flex_cell {
	padding: 0px !important;
}
</style>
<script>
jQuery(document).ready(function($){
	if (window.location.href.indexOf("?bypass=true") > -1) {
	}
	else {
		$('#optinModal').modal({
			backdrop:'static',
			keyboard:false,
			show:true
		});
	}
	$('#_form_105_').validate({ // initialize the plugin
        rules: {
            firstname: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            "field[15]": "required",
            "field[16]": {
                required: "Please provide the secret password",
				minlength: 10,
				equalToIgnoreCase: "#HiddenPassword"
            }
        }
    });
$(document).on('blur change', '#email', function(e) {
var prospect = $(this).val();
var referrer = $('#referrerEmail').val();
if(prospect.toLowerCase() == referrer.toLowerCase()) {
$(this).val('');
alert('You can not refer yourself.');
}
});
});
</script>
<?php
session_start();
/*
 * Easy PHP Tail 
 * by: Thomas Depole
 * v1.0
 * 
 * just fill in the varibles bellow, open in a web browser and tail away 
 */
#$logFile = "log_data.log"; // local path to log file
#$logFile = "../../apache/logs/access.log"; // local path to log file
$logFile = '/var/www/html/failovertests/uploads/'.$_SESSION['filename'].'/log.txt';
#$logFile = '/var/www/html/failovertests/uploads/204.125.212.125_03-23-17_03-58-37/log.txt';
$interval = 10; //how often it checks the log file for changes, min 100
$textColor = ""; //use CSS color

echo "logfile ".$logFile;
#$logFile = '/var/www/html/failovertests/uploads/asssd/log.txt';
// Don't have to change anything bellow
if(!$textColor) $textColor = "blue";
if($interval < 100)  $interval = 100; 
if($_GET['getLog']){
	echo file_get_contents($logFile);
}else{
?>
<html>
	<title>Log</title>
	<style>
		@import url(http://fonts.googleapis.com/css?family=Ubuntu);
		body{
			background-color: white;
			color: <?php echo $textColor; ?>;
			font-family: 'Ubuntu', sans-serif;
			font-size: 16px;
			line-height: 20px;	
		}
		h4{
			font-size: 18px;
			line-height: 22px;
			color: #353535;
		}
		#log {
			position: relative;
			top: -34px;
		}
		#scrollLock{
			width:2px;
			height: 2px;
			overflow:visible;
		}
	</style>
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js" type="text/javascript"></script>
	<script>
		setInterval(readLogFile, <?php echo $interval; ?>);
		window.onload = readLogFile; 
		var pathname = window.location.pathname;
		var scrollLock = false;
		
		$(document).ready(function(){
			$('.disableScrollLock').click(function(){
				$("html,body").clearQueue()
				$(".disableScrollLock").hide();
				$(".enableScrollLock").show();
				scrollLock = false;
			});
			$('.enableScrollLock').click(function(){
				$("html,body").clearQueue()
				$(".enableScrollLock").hide();
				$(".disableScrollLock").show();
				scrollLock = true;
			});
		});
		function readLogFile(){
			$.get(pathname, { getLog : "true" }, function(data) {
				data = data.replace(new RegExp("\n", "g"), "<br />");
		        $("#log").html(data);
		        
		        if(scrollLock == true) { $('html,body').animate({scrollTop: $("#scrollLock").offset().top}, <?php echo $interval; ?>) };
		    });
		}
	</script>
	<body>
	<h4><?php echo $logFile; ?></h4>
		<div id="log">
			
		</div>
		<div id="scrollLock"> <input class="disableScrollLock" type="button" value="Disable Scroll Lock" /> <input class="enableScrollLock" style="display: none;" type="button" value="Enable Scroll Lock" /></div>
	</body>
</html>
<?php  } ?>

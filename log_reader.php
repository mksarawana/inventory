<?php

    $position = 0;
    $newPosition = 0;
    $data = '';
    $filename = '';
    if(isset($_REQUEST['filename'])){
        $filename = '/var/www/html/test_tart/inventory/uploads/'.$_REQUEST['filename'].'/log.txt';
    
        $fp = fopen($filename, 'r');
        
        if(isset($_REQUEST['seekPosition']))
            $position = $_REQUEST['seekPosition'];
        
        if($fp){
            if($position > 0){
                fseek($fp, $position);
            }
            
            $data = fread($fp, filesize($filename));
            
            $newPosition = ftell ( $fp );
            $response = array(  
                'success' => true,
                'message' => $data,
                'seekPosition' => $newPosition
            );
            echo json_encode( $response );
        }else{
            $response = array(  
                'success' => false,
                'message' => 'An error has occurred! Unable to open the file.',
                'seekPosition' => $newPosition
            );
            echo json_encode( $response );
        }
        fclose($fp);
    }else{
        echo "file name is missing";
    }
    
?>
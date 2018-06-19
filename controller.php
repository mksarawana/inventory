  <?php
session_start();
    parse_str($_SERVER['QUERY_STRING']);
    if(isset($action)){
        switch($action){
            case "generateLogFolderName" :
                    $timestamp = date("d-m-Y_h-i-s");
                    $filename = $primary.'_'.$timestamp;
                    $response = array(
                        'success'   => true,
                        'filename'  => trim($filename)
                    );
                break;
			case "generateLogFolderNameForBulk" :
                    $timestamp = date("d-m-Y_h-i-s");
                    $filename = $userid.'_'.$timestamp;
                    $response = array(
                        'success'   => true,
                        'filename'  => trim($filename)
                    );
                break;
            case "uploadfile"   :   
                if ( !empty( $_FILES ) ) {
                    
                    $tempPath = $_FILES[ 'file' ][ 'tmp_name' ];
                    $uploadPath = dirname( __FILE__ ) . DIRECTORY_SEPARATOR . 'uploads' . DIRECTORY_SEPARATOR . $_FILES["file"]["name"];
                    
                    $result = move_uploaded_file( $tempPath, $uploadPath );
                     
                    if($result){
                        $response = array(  
                                            'success' => true,
                                            'message' => 'File uploaded successfully.' 
                                        );
                    }else{
                        $response = array( 
                                            'success' => false,
                                            'message' => 'Error: File could not be uploaded!' 
                                        );
                    }
                    
                }else{
                    $response = array( 
                                        'success' => false,
                                        'message' => 'No files selected!' 
                                    );
                }
                break;

            case "executetests" :
                $command = 'python /var/www/html/test_tart/inventory/';
				
				if($mode == "single"){
                    $command .= 'afo_test.py '.$primary.' '.$secondary.' '.$filename.' 2>&1';
                 }else if($mode == "bulk"){
					$command .= 'inv_format3.py '.$filename.' '.$logFolderName.' 2>&1';
				 }
                    
                exec($command, $output, $returnVal);
                #if($returnVal){
                    
                    //Process filename from the last line of the log.
                    $tempFileName = '';
                    $logWithZipFileName = (is_array($output))?end($output):"";
                    #$logWithZipFileName = "('File saved path : ', '/var/www/html/failovertests/logs/filename.tar.gz')";
                    if($logWithZipFileName!="" && strpos($logWithZipFileName, '.tar.gz')!==false){
                        $fileInfo = new SplFileInfo($logWithZipFileName);
                        $fileNameArray = explode(".tar.gz",$fileInfo->getFilename());
                        $tempFileName = $fileNameArray[0].'.tar.gz';
                    }

                    $response = array(
                        'success'   => true,
                        'name'      => trim($tempFileName),
                        'content'   => implode("\n", $output),
                        'message'   => 'Process execution triggerred successfully!'
                    );
                /* }else{
                    $response = array( 
                        'success'   => false,
                        'message'   => 'Process terminated unexpectedly!'
                    );
                } */
                
                break;
            
            case "download"     :   
                $zip = dirname( __FILE__ ) . DIRECTORY_SEPARATOR . 'logs'. DIRECTORY_SEPARATOR . $filename;
                if (file_exists($zip)) {
                    header($_SERVER["SERVER_PROTOCOL"] . " 200 OK");
		    header("Content-Encoding: gzip");
                    header("Cache-Control: public"); // needed for internet explorer
                    header("Content-Type: application/x-zip");
                    header("Content-Disposition: attachment; filename=".basename($zip));
                    readfile($zip);
                    die();
                } else {
                    die("Error: File not found.");
                }
                break;
                
            default:
                $response = array( 
                                'success' => false,
                                'message' => 'Error: Invalid value passed for required parameter!' 
                            );
        }
    }else{
        $response = array( 
                        'success' => false,
                        'message' => 'Error: Missing required parameter!' 
                    );
    }
        
    echo json_encode( $response );
    exit;
?>

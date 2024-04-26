when the code migrate from one vm to other please make sure of below things

1) in the createFolder() ,get_article_ids(), function make sure to change the path variables
     path = "C:/PCMDWD"
     path = "C:/PCMDWD/database"
     
2) Make sure to provide the hsdes handle path 
3) In enviroment make sure to change the python version and with appropriate python path 

#changes for tommorwos tcd owners presentation
1) changes the keyword mapped column basesd on space seperated





    <!-- 
    <form method="post" action="{{ url_for('web.pcmd_dashboard')}}" >
        <div class="d-flex  flex-wrap mt-3 justify-content-between align-items-center">
            <h4 class="p-1 " id="heading" style="margin-left:340px ;">
                Specify article_id or query_id for hardware details
            </h4>       
        </div>
        <hr class="text-muted mb-4">
        <div class="row mb-4 justify-content-center">
            <label for="Query_Id" class="col-xs-12 col-md-3"  style="font-size: 20px"> Query_Id :   </label>
            
        </div>
        <div class="row mb-3 justify-content-center">
            <input type="text" class="col-xs-12 col-md-3"  pattern="\d{11}" name="query_id" style="width:400px ;height:30px">
           
            <label> 
                <input type="radio" name="radio_options" value="option2" checked>Config to Test_Case mapping
            </label>
          
            <label>
                <input type="radio" name="radio_options" value="option1">Test_Case to Config mapping
            </label>
           
        </div>
            
        <div class="row mb-3 justify-content-center">
            <label  class="col-xs-12 col-md-3"  style="font-size: 20px" >Test Case/Article_Id :</label>
        </div>
       
        <div class="row mb-3 justify-content-center" >
            <input class="col-xs-12 col-md-3" type="text" name="article_id"   style="width:400px ;height:30px"> 
        </div>

        <div class="row mb-3 justify-content-center my-2 mx-6">
            <button type="submit" id="uniqueid" class="btn btn-lg btn-success col-xs-12 col-md-4 my-3 mx-4"  style="width:200px">Submit</button>
            
        </div>
      </div>
    </form>
  -->
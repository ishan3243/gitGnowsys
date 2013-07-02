
 $.noConflict();
   var isWikipage=false;
   var editWikipage=false;
   var objid;
   var isSection=false;
   var editSection=false;
   var isSubsection=false;
   var editSubsection=false;
   var isNode=false; 
   var isObject=false;
   var isTwist=false;
   var isThread=false;
   var isResponse=false;
   var editTwist=false;
   var editThread=false;
   var editResponse=false;
   var editImage=false;
   var isImage=false;
   var isVideotitle=false;
   var isEditdoc = false;

   function subsecsave(objid){
       var org_data = $("#gnoweditor").val();
       var encode_data = encodeURIComponent(org_data);
       var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
       $("#sectionreply"+objid).val(decode_data);
       $("#subsecsubmit"+objid).trigger('click');
       $(".savesubsec1").hide();
       
   }
function moveUp() {
    
        $('#lstBox1 :selected').each(function (i, selected) {
            $(this).insertBefore($(this).prev());
	    $("#lstbox2").options.att("selected",false);
        });
        $('#lstBox1 select').focus().blur();
      $('#lstBox2 :selected').each(function (i, selected) {
            $(this).insertBefore($(this).prev());
	  $("#lstbox1").options.att("selected",false);
        });
        $('#lstBox2 select').focus().blur();
}

function moveDown() {
    $('#lstBox1 :selected').each(function (i, selected) {
        $(this).insertAfter($(this).next());
	$("#lstbox2").options.att("selected",false);	
    });
    $('#lstBox1 select').focus().blur();
       $('#lstBox2 :selected').each(function (i, selected) {
            $(this).insertAfter($(this).next());
	   $("#lstbox1").options.att("selected",false);
        });
        $('#lstBox2 select').focus().blur();
    }

    
  jQuery(document).ready(function($) {
        $('#btnUp').click(moveUp);
     	 $('#btnDown').click(moveDown);
        $("#addcontent").one("click",function(){
 	
	   isSection=true;
	          $("#addcontent").hide();
	          //$("#save").show();
		  $("#chart").hide();
	    $("#content").css({"width":"300px",})
	         document.getElementById('gnoweditor').style.visibility="visible";
	        $("#gnoweditor").orgitdown(mySettings);
		 var orgtext = $("#gnoweditor").val();

	   });
	$("#save").one("click",function() {
		var org_data = $("#gnoweditor").val();
		document.getElementById("orgpage").value = org_data;
		var encode_data = encodeURIComponent(org_data);
		$('#submitsec').trigger('click');
	    $("#save").hide();
		});
	$("#cancel").one("click",function() {
	    $("#collection").hide();
	    });
	$("#pagecontent1").one("click",function() {
 	    $(this).replaceWith('<textarea id="gnoweditor" style="visibility:hidden;width:450px"></textarea>');
	    isWikipage=true;
	    $("#chart").hide();
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            $(".orgitdownContainer").css({"margin-top":"0px","margin-left":"10px"});
	//$("#save1").show();
	    $("#pagecontent1").hide();
	    $("#content").css({"width":"300px",})
	    });
        $("#save1").one("click",function() {
	var org_data = $("#gnoweditor").val();
	document.getElementById("orgpage1").value = org_data;
	var encode_data = encodeURIComponent(org_data);

	$(".orgitdownContainer").hide();
	$("#pagedata").val(encode_data);
	if ($("#coll").is(":checked")) {
		}
	    else {
		 $('#submitpage').trigger('click');}


	});
      $(".editseccontent").one("click",function(){
          editSection=true;
	 // $(".saveseccontent").show();
	   $("#content img").css({"max-width":"600px",})
	   $("#content").css({"width":"600px",})
	  $("#chart").hide();
	  document.getElementById('gnoweditor').style.visibility="visible";
	  $("#gnoweditor").orgitdown(mySettings);
	  var a = this.name;
	  $("#gnoweditor").val(a);
	  var elmts = document.getElementsByClassName("editval");
	  for (var i = 0; i < elmts.length; i++){
	      elmts[i].setAttribute("value","edited");}
	  var screenTop = $(document).scrollTop();
	  $(".orgitdownContainer").css({
	      "margin-top":screenTop,});
	  $("#newsection1").hide();
	  $(".editseccontent").hide();
	  $(".createsubsection").hide();
	  $("#rating").hide();
	  $(".chkbox").hide();
	  $(".deletesec").hide();
	  $(".tag").hide();
	  $(".tagtext").hide();
	  $(".editpagecontent").hide();
	  $(".editsubsec").hide();
      });
       $(".saveseccontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   var encode_data = encodeURIComponent(org_data);
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",decode_data);}
	   $(".submitresponse").trigger('click');
	   $(".saveseccontent").hide();
		  
       });

       $(".editsubsec").one("click",function(){
	   editSubsection=true;
	   var each_id=$(this).attr("id");
	   $("#chart").hide();
	   $("#content img").css({"max-width":"600px",});
	   
	   $("#content").css({"width":"600px",});
	   document.getElementById('gnoweditor').style.visibility="visible";
	   $("#gnoweditor").orgitdown(mySettings);
	   var org_data=$("#subsec"+each_id).val();
	   $("#edit"+each_id).val("edited");
	   $("#sectionreply"+each_id).val(org_data);
	   $("#gnoweditor").val(org_data);
	   var screenTop = $(document).scrollTop();
	   $(".orgitdownContainer").css({
	       "margin-top":screenTop,});
	    //$("#save"+each_id).show();
	   objid=each_id;
	   $(".editsubsec").hide();
	   $(".submitsubsec1").hide();
	   $(".tag").hide();
	   $(".tagtext").hide();
	   $(".editpagecontent").hide();
	   $("#newsection1").hide();
	   $(".editseccontent").hide();
	   $(".createsubsection").hide();
	   $("#rating").hide();
	   $(".chkbox").hide();
	   $(".deletesec").hide();
       });

       var pageid=(location.href.split("/"))[6];
       $(".editpagecontent").one("click",function(){
	tObjName = '';
	
	   //alert('helooooo');
	  //  $("#requestHeading").show();
	    //$("#dynamic").show();
	    //$(".sendRequest").show();
	   // $("#hiddenButton2").trigger("click");
	    $(this).replaceWith('<textarea id="gnoweditor" style="visibility:hidden;width:450px"></textarea>');
	    
	    editWikipage=true;
      	    $("#chart").hide();
	    $(".editpagecontent").hide();
      	  //  $(".savepagecontent").show();
 	    $("#content img").css({"max-width":"600px",});
	  
	    $("#content").css({"width":"600px",});
	    $("#gnoweditor").orgitdown(mySettings);
	    $.post('/textb/editButton/',{pageid:pageid},function(data,status){		
		if(status=="error")	alert("no!!!!!!");
		else {$(".orgitdownEditor").attr("id",data);   tObjName= tObjName+data;   }
		});
	       //textb	    
		
            document.getElementById($(".orgitdownEditor").attr("id")).style.visibility="visible";
            var a = this.name;
	    $("#"+$(".orgitdownEditor").attr("id")).val(a);
	    var elmts = document.getElementsByClassName("editval");
	    for (var i = 0; i < elmts.length; i++){
		elmts[i].setAttribute("value","edited");}
	   //var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":"0px","margin-left":"10px"});
	   //$(".tag").hide();
	   //$(".tagtext").hide();
	   $("#newsection1").hide();
	   $(".createsubsection").hide();
	   $("#rating").hide();
	   $(".chkbox").hide();
	   $(".deletesec").hide();
	   $(".editseccontent").hide();
	   $(".editsubsec").hide();
	mobwrite.syncGateway = '/textb/mobwrite/';



   	/*$("#gnoweditor").load(function() {
        	mobwrite.share('gnoweditor');
    	});*/

    	var iframe = document.getElementById($(".orgitdownEditor").attr("id"));
   	 iframe.onkeypress = function () {	
	
      // Is the sync gap big? and do we have a sync in transit?
      if ((mobwrite.syncInterval > 1000) && (mobwrite.syncKillPid_==null)) {
        // Stop the current timer, run a sync, and start the timer again.
        window.clearTimeout(mobwrite.syncRunPid_);
        mobwrite.syncRun1_();
        mobwrite.syncRunPid_ = window.setTimeout(mobwrite.syncRun1_,mobwrite.syncInterval);
         }
       };
    //alert($(".orgitdownEditor").attr("id"));	
    //alert($(".orgitdownEditor").attr("id"));	
     setTimeout(function(){
     $("#groups").show();
     $.post('/textb/getAllGroups/',{pageid:pageid ,filename:$(".orgitdownEditor").attr("id") },function(data,status){
		if(status=="error") alert("Status: "+status);
		else
		{	
			var len1=data.length;			
			for(i=0;i<len1;i++)
			{	
				if(i==0)  var str="<ul>Your Group</ul>";
				else	  var str="<ul>Other Group</ul>";
				var len=data[i].length;
				for(j=0;j<len;j++)
				{
					position=str.length-5;
					str=[str.slice(0, position),"<li>"+data[i][j]+"</li>", str.slice(position)].join('');				
				}
				$("#currentGroups").append(str);
						
			}		
		}
		
	});
},4000);  
  
    setTimeout(function(){mobwrite.share($(".orgitdownEditor").attr("id"))},2000);   //textb
   
    /* insert 4 spaces instead of leaving textarea */
    function insertTab(e) {
        if (e.keyCode == 9) {
            var tab = "    ";
            var txt = e.currentTarget;
            var pos = txt.selectionStart;
            var scrollTop = txt.scrollTop;
            txt.value = txt.value.substring(0, pos) + tab + txt.value.substring(txt.selectionEnd, txt.textLength);
            txt.focus();
            txt.selectionStart = pos + tab.length;
            txt.selectionEnd = pos + tab.length;
            txt.scrollTop = scrollTop;
            return false;
        }
        return true;
    }
    $(".orgitdownEditor").keydown(insertTab);   //textb

	  
          $("#hiddenButton").trigger('click');   
	$("#invite").show();
	$("#dy").trigger('click');

});
	



	$(".addtodrawer").click(function(){
	alert("test");
	  
	  // var ptitle=document.getElementById("ptitle").value;
	  $(".addtodrawer").hide();
	  var getdrawer=$(".getdrawer").val();
	  $("#collection").show();
	  
       });


      $("#resetdrawer").click(function(){
	  $('#lstBox2').empty();
      });

     
        $('#btnRight').click(function(e) {
        var selectedOpts = $('#lstBox1 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }

        $('#lstBox2').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
      $('#btnLeft').click(function(e) {
        var selectedOpts = $('#lstBox2 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }

        $('#lstBox1').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });

   	
       $(".savepagecontent").one("click",function(){
	 var isOwner;
	 $.post('/textb/checkOwner2/',{textObjName:$(".orgitdownEditor").attr("id")},function(data){isOwner=data;

		if(isOwner==1)	
		{	
	  		 mobwrite.unshare($(".orgitdownEditor").attr("id"));    //textb
	   
		
			$.post('/textb/deleteLink/',{textObjName:$(".orgitdownEditor").attr("id")},function(data,status){
			if(data==='DS') 
			{		
				alert("Your work has been published");
				var org_data = $(".orgitdownEditor").val();   //textb
			  	 var elmts = document.getElementsByClassName("reptext");
			  	 var encode_data = encodeURIComponent(org_data);
			  	 var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
			  	 for (var i = 0; i < elmts.length; i++){
			  	 elmts[i].setAttribute("value",decode_data);}
		          	 $(".pagedit").trigger('click');
			  	 $(".savepagecontent").hide();
			  	 $(".orgitdownContainer").hide();		
			}		
			else alert('Error: '+status);	
		  
		});
		}   
	
		else alert("You don't have enough privelages to save this file ");

});   
	});


      $("#editnodecontent").one("click",function(){
	  isNode=true;
      	    $("#chart").hide();
	    $("#content img").css({"max-width":"600px",})
	   
	    $("#content").css({"width":"600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            var a = this.name;
	 
	    $("#gnoweditor").val(a);
	   var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":screenTop,});
	   $("#editnodecontent").hide();
	   //$("#savenodecontent").show();
           $("#nodedit").hide();
		    
       });
       $("#savenodecontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var encode_data = encodeURIComponent(org_data);
	  
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   $("#reptext").val(decode_data);
	   $("#nodedit").trigger('click');
	   $("#nodedit").hide();
	   
       });


      $("#editobjectcontent").one("click",function(){
	  isObject=true;
      	    $("#chart").hide();
	    $("#content img").css({"max-width":"600px",})
	   
	    $("#content").css({"width":"600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            var a = this.name;
	 
	    $("#gnoweditor").val(a);
	   var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":screenTop,});
	   $("#editnodecontent").hide();
	   //$("#savenodecontent").show();
           $("#objectedit").hide();
		    
       });
       $("#saveobjectcontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var encode_data = encodeURIComponent(org_data);
	  
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   $("#reptext").val(decode_data);
	   $("#objectedit").trigger('click');
	   $("#objectedit").hide();
	   
       });
       $(".createsubsection").one("click",function(){
	           isSubsection=true;
	           //$(".savesubsec").show();
	           //$(".submitsubsec").show();
	           $(".createsubsection").hide();

	           $("#content img").css({"max-width":"600px",})
	           $("#content").css({"width":"600px",})   
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    $("#gnoweditor").val('');
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
	   });
       $(".savesubsec").one("click",function() {
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   var encode_data = encodeURIComponent(org_data);
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",decode_data);}
	   $(".savesubsec").hide();
	   $(".submitsubsec").trigger('click');
       });

      $("#savecontent").one("click",function() {
	      var org_data = $("#gnoweditor").val();
	      var id =  document.getElementById("objectid").value
	       document.getElementById("orgcontent").value = org_data;
	      var encode_data = encodeURIComponent(org_data);
          $("#savecontent").hide();
		         $.ajax({
			       url: '/nodetypes/ajax/contentorgadd/?id=' + id + '&contentorg=' + encode_data,
			       success: function(data) {
			         $.ajax({
				    url: '/nodetypes/ajax/ajaxcreatefile/?id=' +id+ '&content_org=' +encode_data,
				    success: function(data) {
				    	$.ajax({
				    		url: '/nodetypes/ajax/ajaxcreatehtml/',
				    		success: function(data) {
				    		    $.ajax({
				    			    url: '/nodetypes/ajax/contentadd/?id=' +id,
                                                            success: function(data) {
								// alert("Data Saved");
                                                              location.reload();}
				    			});
				    		}      
				     	    });
				     }
				}); 
			    
			       }
			 });
		    
      });

  });
       
    

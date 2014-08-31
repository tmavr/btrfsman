#!/usr/bin/perl
# btrfsman_sub.cgi
# BTRFS Manager - Subvolume Management

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'sub_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$volume =  $in{'volume'};
$opt = $in{'opt'};



if ($volume =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe mountpoint";
}

if (($act) && ($volume) ) {
  #if ($newlabel) {
    print "<p> Taking Action Executing Command:#", $text{'txt_p'};
    $cmd= " btrfs $act $opt \"$volume\"";
    print $cmd, $text{'txt_p'};
    $result=`$cmd`;
    
    print $result, $text{'sub_operation'}, $text{'txt_p'} ;
  #}
}
else{
	
	subvolume_menu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');


=head1 subvolume_menu

Display subvolume menu

=cut
sub subvolume_menu {
  print $text{'sub_h'};
  $result = `mount |grep btrfs`;
  $result =~  s/\n/<br>/g;
	
  @splitres = split /<br>/, $result;
  print $text{'index_youhave1'}, scalar (@splitres), $text{'index_youhave3'};
  $subvolcount=0;
  $did=0;
  for (@splitres){
    print ui_columns_start([ @splitres[$did], ""]);
    $drivea = @splitres[$did];
    @driveb = split /on /, $drivea;
    @drivec = split / /, @driveb[1];
    @mountedrive[$did] =  @drivec[0];
    print ui_columns_row([$text{'index_mountp'}, @mountedrive[$did]]) ;

    $result = `btrfs subvolume list @mountedrive[$did]`;
    $slist= $result;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfssl'}, $result]);
    print ui_columns_end();
    
      
    if ($result){
    	
    	@subvol1 = split /\n/,$slist;
    	$did2=0;
      for (0..scalar(@subvol1)-1){
    	  @subvol2=split /path /,@subvol1[$did2];
        #print "##",@mountedrive[$did], @subvol2[1], "##";
        
        $subvolcount++;
        @subvolpath[$subvolcount] = @mountedrive[$did] . "/" . @subvol2[1];
        
        #print ui_buttons_start();
    	  #print ui_buttons_row("btrfsman_sub.cgi",  $text{'sub_bt_delete'},  $text{'sub_bt_delete_help'}, ui_textbox('showsub', @subvolpath[$subvolcount],40,1), ui_hidden('act', 'subvolume delete'), ui_hidden('volume', @subvolpath[$subvolcount]), ui_textbox('opt',''));
    	  #print ui_buttons_end();
    	
        $did2++;
      }   
    	
    	
    }
    
    print $text{'txt_p'};

    $did++;
  }
  
  print $text{'index_youhave1'}, scalar( @subvolpath)-1, "volumes</b><p>", @subvolpath , "<p>";
  
  
  print "<p><h1>Expert Subvolume Create</h1><p>";
  print "Input Subvolume MoutnPoint and click button<p>";
  print ui_buttons_start();
  print ui_buttons_row("btrfsman_sub.cgi",  $text{'sub_bt_create'},  $text{'sub_bt_create_help'}, ui_textbox('volume', '/mnt/',20,0), ui_hidden('act', 'subvolume create') );
  print ui_buttons_end();
  
  print "<p><h1>Expert Subvolume Delete</h1><p>";
  print "Select Subvolume MountPoint and click button<p>";
  print ui_form_start("btrfsman_sub.cgi");
  
  print ui_hidden('act', 'subvolume delete'),  ui_textbox('opt',''), "Options", $text{'txt_p'};
  print ui_select('volume', 1, [@subvolpath] ), $text{'txt_data'}, $text{'txt_p'};

  print ui_form_end( [[undef, $text{'sub_bt_delete'}]] );
  
  
  print "<p><h1>Expert Subvolume Snapshot Create</h1><p>";
  print "Select Subvolume MountPoint and click button<p>";
  print ui_form_start("btrfsman_sub.cgi");
  
  print ui_hidden('act', 'subvolume snapshot '), $text{'txt_p'};
  print ui_select('opt', 1, [@subvolpath] ), "Source", $text{'txt_p'};
  print ui_textbox('volume', '/mnt/' ), "Destination", $text{'txt_p'};
  
  print ui_form_end( [[undef, $text{'sub_bt_snapshot'}]] );
}

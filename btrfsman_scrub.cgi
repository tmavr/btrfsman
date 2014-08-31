#!/usr/bin/perl
# btrfsmanscrub.cgi
# BTRFS Manager - Scrubbing

require './btrfsman-lib.pl';
&ReadParse();


ui_print_header(undef, $text{'scrub_title'}, "", undef, 1, 1);

$act = $in{'act'};
$mp =  $in{'mp'};
$ro = $in{'ro'};

if ($act) {
  if (($mp) && ($ro)) {
    print "$in<p>Taking Action Executing Command:#";
    if ($ro eq 'ro'){
    	$cmd= "btrfs scrub $act $mp -R 2>&1";
    	print  $text{txt_executing}, $cmd, $text{'txt_p'};
    	$result = `$cmd`;
    	print $result;
    } else {
    	if ($ro eq 'rw'){
      	$cmd= "btrfs scrub $act $mp 2>&1";
      	print  $text{txt_executing}, $cmd, $text{'txt_p'};
      	$result = `$cmd`;
        print $result;
    	}
    }
  }
}

scrub_menu();

ui_print_footer('/', 'Webmin index', '', 'Module menu');


=head1 balancemenu

Display scrub menu

=cut
sub scrub_menu {
  print $text{'scrub_mounted_h'};
  $result = `mount |grep btrfs`;
  $result =~  s/\n/<br>/g;
	
  @splitres = split /<br>/, $result;
  print $text{'index_youhave1'}, scalar (@splitres), $text{'index_youhave3'};
  $did=0;
  for (@splitres){
    print ui_columns_start([ @splitres[$did], ""]);

    if (@splitres[$did] =~ /(ro)/) {
      print ui_columns_row([$text{'txt_warn'}, $text{'txt_warn_ro'}]);
    }    
    
    $drivea = @splitres[$did];
    @driveb = split /on /, $drivea;
    @drivec = split / /, @driveb[1];
    @mountedrive[$did] =  @drivec[0];
    $result = `btrfs scrub status @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsss'} , $result]);

    $result = `btrfs scrub status @mountedrive[$did] -R`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsss'} , $result]);

    if ($result =~ /no stats available/) {
      print ui_columns_row([$text{'txt_warn'}, $text{'txt_warn_noscrub'}]);
    }
    
    if (! (($result =~ /read_errors: 0/) && ($result =~ /csum_errors: 0/) && ($result =~ /verify_errors: 0/) && ($result =~ /super_errors: 0/) && ($result =~ /malloc_errors: 0/)  && ($result =~ /uncorrectable_errors: 0/) && ($result =~ /unverified_errors: 0/))) {
      print ui_columns_row([$text{'txt_warn'}, $text{'txt_warn_scruberrors'}]);
    }
    
    
    print ui_columns_end();

    print ui_buttons_start();
    print ui_buttons_row('btrfsman_scrub.cgi', $text{'scrub_bt_start'}, $text{'scrub_bt_start_help'}, ui_hidden('act', 'start'), ui_hidden('mp', @mountedrive[$did]), ui_radio("ro", "ro",
[ [ 'ro', 'ro' ],
[ 'rw', 'rw' ] ] ));

    print ui_buttons_row('btrfsman_scrub.cgi', $text{'scrub_bt_stop'}, $text{'scrub_bt_stop_help'}, ui_hidden('act', 'stop'), ui_hidden('mp', @mountedrive[$did]), ui_radio("conf", 0,
[ [ 1, 'Confirm' ],
[ 0, 'Cancel' ] ] ));

    print ui_buttons_row('btrfsman_scrub.cgi', $text{'scrub_bt_resume'}, $text{'scrub_bt_resume_help'}, ui_hidden('act', 'resume'), ui_hidden('mp', @mountedrive[$did]));


    print ui_buttons_end();

    print "<p><p>";

    $did++;
  }

}

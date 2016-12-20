#!/usr/bin/env perl
use strict;
use LWP::UserAgent;

my ($testcount) = (0);
my ($ua, $header, $request, $response);
my $baseurl_location = "http://localhost:8000/xsede-api/provider/ipf-glue2/v1/location/";
my ($cred) = ('test/pass');

my $seed_id = 'urn:glue2:Location:XSEDETestingComputingCenter';
my $seed_doc = '{"ID":"' . $seed_id . '","ResourceID":"testing.xsede.org","Name":"XSEDE Testing Computing Center","CreationTime":"2013-04-28T16:22:02Z","EntityJSON":{"testing":"value"}}';

$ua = LWP::UserAgent->new;

test_delete( title => 'DELETE document if it exists (MAY fail)',
	     url => "${baseurl_location}ID/$seed_id/",
	     cred => $cred);

test_delete( title => 'DELETE document if it exists (MUST fail)',
	     url => "${baseurl_location}ID/$seed_id/",
	     cred => $cred);

test_delete( title => 'DELETE document with invalid credentials (MUST fail)',
	     url => "${baseurl_location}ID/$seed_id/",
	     cred => 'not/real');

test_post( title => 'POST document#1 to invalid URL (MUST fail)',
           url => "${baseurl_location}ID/$seed_id/",
	   doc => $seed_doc);

test_post( title => 'POST document#1',
	   url => "$baseurl_location",
	   doc => $seed_doc);

test_post( title => 'POST document#1 again (MUST fail)',
	   url => "$baseurl_location",
	   doc => $seed_doc);

my $result = test_get( title => 'GET non-existent document (MUST fail)', url => "${baseurl_location}ID/$seed_id$seed_id/");

my $result = test_get( title => 'GET document#1', url => "${baseurl_location}ID/$seed_id/");
print "$result\n" . (($seed_doc eq $result) ? "Document match\n" : "FAILED DOCUMENT MATCH\n");

my $seed_doc2 = '{"ID":"' . $seed_id . '","ResourceID":"testing.xsede.org","Name":"XSEDE Testing Computing Center","CreationTime":"2013-04-28T16:22:02Z","EntityJSON":{"testing":"UPDATEDvalue"}}';

test_put( title => 'PUT/update document#1',
	  url => "${baseurl_location}ID/$seed_id/",
	  doc => $seed_doc2);

my $result2 = test_get( title => 'GET updated document#1', url => "${baseurl_location}ID/$seed_id/");
print "$result2\n" . (($seed_doc2 eq $result2) ? "Document match\n" : "FAILED DOCUMENT MATCH\n");

my $result3 = test_get( title => 'GET all documents', url => "$baseurl_location");
print "$result3\n";
exit 0;

sub print_header {
    $testcount++;
    print "*** TEST $testcount (" . shift . ") ***\n";
}

sub test_delete {
   my %args = @_;
   print_header($args{title});
   my ($url) = $args{url};
   print "DELETE $url\n";
   $request = HTTP::Request->new('DELETE', $url);
   $request->authorization_basic(split('/', $args{cred}));
   $response = $ua->request($request);
   if ($response->is_success) {
       print 'Passed rc=' . $response->code() . "\n";
   } else {
       print '*FAIL* rc=' . $response->status_line() . "\n";
   }
}

sub test_post {
   my %args = @_;
   print_header($args{title});
   my ($url, $doc) = ($args{url}, $args{doc});
   print "POST $url\n";
   $header = HTTP::Headers->new(Content_Type => 'application/json');
   $request = HTTP::Request->new('POST', $url, $header, $doc);
   $request->authorization_basic('test', 'pass');
   $response = $ua->request($request);
   if ($response->is_success) {
       print 'Passed rc=' . $response->code() . "\n";
   } else {
       print '*FAIL* rc=' . $response->status_line() . "\n";
   }
}

sub test_put {
   my %args = @_;
   print_header($args{title});
   my ($url, $doc) = ($args{url}, $args{doc});
   print "PUT $url\n";
   $header = HTTP::Headers->new(Content_Type => 'application/json');
   $request = HTTP::Request->new('PUT', $url, $header, $doc);
   $request->authorization_basic('test', 'pass');
   $response = $ua->request($request);
   if ($response->is_success) {
       print 'Passed rc=' . $response->code() . "\n";
   } else {
       print '*FAIL* rc=' . $response->status_line() . "\n";
   }
}


sub test_get {
   my %args = @_;
   print_header($args{title});
   my ($url) = ($args{url});
   print "GET $url\n";
   $request = HTTP::Request->new('GET', $url);
   $response = $ua->request($request);
   if ($response->is_success) {
       print 'Passed rc=' . $response->code() . "\n";
       return $response->content();
   } else {
       print '*FAIL* rc=' . $response->status_line() . "\n";
   }
}

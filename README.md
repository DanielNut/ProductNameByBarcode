# ProductNameByBarcode

1. When you run project you have to have
instances_fmcg_mining1.txt file with every string have structure like this:
SOMEFING SOMETHING BARCODE ...
Third column must be barcode so script can operate with that.
This file has to be in the same directory as other stuff here.
2. After file prepared, use python main.py command to execute script.
It will try to scrape couple of websites to get name of product with that barcode.
All names will be in russian or ukrainian.


In this version project may include some of hand work of you:

(1) For example if you have same barcode twice in the instances_fmcg_mining1.txt file, it will jump to 
last string and you'll have to manually write the last parsed string index of this file(instances_fmcg_mining1.txt) to number_of_parsed_barcodes.csv
to continue. You also have to set it to 0 before start with new data.

(2) Sites may block you because of many queries. In that case you will have to continue manually for some time or simply wait. 
For process barcode and name manually just use command.
python process_barcode.py -n <name> -b <barcode>
It will add barcode and name to result.csv file and update the index of last processed barcode, but be careful, it can have problem similar to (1).
  
(3) Sites may not have this barcode in their database and you may want to add barcodes to not found for further searching. 
 In this case we have not_found_codes.txt. To add barcode to that file just use command
  python process_barcode.py -b <barcode>
It will add barcode to not_found_codes.txt and update the index of last processed barcode, but be careful, it can have problem similar to (1).


All results are in result.csv file.


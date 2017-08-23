import sys, re, csv, os

def read_mp_data(filename):
	with open(filename, "rU", encoding="ISO-8859-1") as handle:
		cnt = 0
		rows = csv.reader(handle)
		mp_dict =  {}
		for row in rows:
			mp_name = row[0]
			twitter_handle = "@" +row[3]
			if len(twitter_handle) > 1 and len(mp_name) > 1:
				mp_dict[twitter_handle] = mp_name
			# if cnt == 4:
			# 	break
			# cnt += 1
	print("no. of MPs disvoered ->", len(mp_dict))
	return mp_dict

def discover_mp_handles(filename, twitter_handle_dict):
	twitter_handle_RE = r"@\w{1,15}"
	twitter_handles = ["Line"]
	twitter_handles.extend(list(twitter_handle_dict.keys()))
	#output file
	with open(filename[:filename.rfind(".")] + '_mentions_3.csv','w') as file:
		# write header file
		file.write(",".join(twitter_handles))
		file.write("\n")

		# input file
		with open(filename, "r", encoding="ISO-8859-1") as handle:
			rows = csv.reader(handle)
			line_num = 0
			skip_header = False

			for row in rows:
				
				if not skip_header:
					skip_header = True
					line_num += 1
					continue

				tweet = row[3]
				mentions_array = ["0"] * len(twitter_handles)
				# find all twitter handles in the line
				handles = re.findall(twitter_handle_RE, tweet)
				mentions_array[0] = str(line_num)
				if handles:
					for h in handles:
						if h in twitter_handle_dict.keys():
							h_ind = twitter_handles.index(h)
							mentions_array[h_ind] = "1"
				file.write(",".join(mentions_array))
				file.write("\n")
				# if cnt == 3:
				# 	break
				line_num += 1
			print(line_num)


if __name__ == "__main__":
	data_filename = sys.argv[1]
	mp_filename = sys.argv[2]
	# read mp data
	mp_data = read_mp_data(mp_filename)
	# find women MP mentions in
	discover_mp_handles(data_filename, mp_data)
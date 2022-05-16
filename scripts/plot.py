import argparse
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sb
import pandas as pd
import os

# styling
sb.set_style("whitegrid")
# sb.set_palette("crest")


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help='log file name')
parser.add_argument("save_as", help='Name of the plot file')
parser.add_argument("-su", '--success', action="store_true", help='success flag')
parser.add_argument("-ws", '--window_size', action="store_true", help='window size flag')
parser.add_argument("-r", '--reward', action="store_true", help='reward flag')
parser.add_argument("-s", '--spl', action="store_true", help='spl flag')
parser.add_argument("-dg", '--distance_to_goal', action="store_true", help='distance_to_goal flag')
parser.add_argument("-al", '--a', action="store_true", help='all flags')
parser.add_argument("-xl", '--xlimit', nargs='?', help='limit on x axis')


args = parser.parse_args()
files = args.files

# no_params_x=[]
# no_params_y=[]

#data dictinary initialization
data={}
fig, ax = plt.subplots()
for file in files:
    data[file] = { 'update':[],'date':[],'window_size':[],'distance_to_goal':[],'reward':[],'spl':[],'success':[]}


for file in files :
    with open(file, 'r') as f:
        for line in f:
            line= line.strip()
            chunks= line.split(" ")
            # if chunks[2] == "agent":
            #     no_params_x.append(chunks[:2])
            #     no_params_y.append(chunks[-1])

            if chunks[2] == "Average":
                date_time_obj = datetime.strptime(' '.join(chunks[:2]), '%Y-%m-%d %H:%M:%S,%f')
                data[file]["date"].append(date_time_obj)
                data[file]["window_size"].append(float(chunks[5]))
                data[file]["distance_to_goal"].append(float(chunks[8]))
                data[file]["reward"].append(float(chunks[11]))
                data[file]["spl"].append(float(chunks[14]))
                data[file]["success"].append(float(chunks[17]))
            if chunks[2] == "update:" and len(chunks) > 5:
                fst_chunk=chunks[3].split('\t')
                data[file]['update'].append(float(fst_chunk[0]))
    f.close()


#find the min xlimit
maxes=[]
for file in files:
    maxes.append(max(data[file]['update']))
print(min(maxes))
ax.set_xlim(0,min(maxes))


#if xlimit is given
if args.xlimit:
    ax.set_xlim(0, float(args.xlimit))


#displaying graph    
for file in files :
    # filename = os.path.splitext(file)[0]
    filename = os.path.splitext(file)[0]
    if (args.success or args.a) :
        ax.plot(data[file]["update"], data[file]["success"], label = filename + "_success")

    # if (args.window_size or args.a) :
        # ax.plot(data["update"], data["window_size"],label="window_size")

    if (args.distance_to_goal or args.a):
        ax.plot(data[file]["update"], data[file]["distance_to_goal"],label=filename+"_distance_to_goal")

    if (args.reward or args.a):
        ax.plot(data[file]["update"], data[file]["reward"],label=filename+"_reward")

    if (args.spl or args.a):
        ax.plot(data[file]["update"], data[file]["spl"],label=filename+"_spl")

leg = ax.legend();
plt.savefig(args.save_as)

# new = pd.DataFrame.from_dict(data)
# sb.set_theme(style="darkgrid")
# sb.lineplot(x = "update", y = "spl", data = new)
# plt.show()

import matplotlib.pyplot as plt
import math
from operator import itemgetter


# read in the values
# gaia values
gaia = open("fehp00afep2.Gaia", "r")

# generated isochrone values
iso = open("tmp1626725669.txt", "r")

#############################
# GAIA BREAKDOWN
# a list of the ages in order
ages = []
# all the data for each age
all_ages = []
gaia_data = [[]]
age = 0
############################
# set all values to none
current_age = 0
G = []
Bp_Rp = []
All_G = [[]]
All_BpRp = [[]]
############################
# isochrone breakdown
iso_G = []
isoBP_RP = []
tally_ages = 0
###########################
age_dist_dict = {}

# a function to calculate distance be
def calculateDistance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

# build the Gaia structures
def buildGaia(age, G, Bp_Rp):
    for line in gaia:
        # if the line contains the age
        #print(line)
        line_list_age = line.strip().split(" ")

        if (len(line_list_age[0]) >= 2 and line_list_age[0][0] == "#" and line_list_age[0][1] == "A" and line_list_age[0][2] == "G"):
            # print(line_list_age[1])
            if(len(line_list_age[0]) == 11):
                age = line_list_age[0][5: 11: 1]
            else:
                age = line_list_age[1]
            # print(age)

            # when we get to a new age, graph it
            if (G != [] and Bp_Rp != []):
                All_G.append(G)
                All_BpRp.append(Bp_Rp)


            # then reset and start with a new age
            # current_age = line_list_age[1]
            ages.append(age)
            G = []
            Bp_Rp = []
            age_data = []

        elif(len(line.strip()) != 0 and (line[0] != "#")):
            line_by_term = line.strip().split(" ")
            line_by_term  = ' '.join(line_by_term).split()
            if (len(line_by_term) >= 8):
                G.append(float(line_by_term[5])) # list of G values
                Bp_minus_Rp = float(line_by_term[6]) - float(line_by_term[7])
                Bp_Rp.append(Bp_minus_Rp)

# Build the isochrone structure
def buildiso():
    for line in iso:
        if(len(line.strip()) != 0 and (line[0] != "#")):
            line_by_term = line.strip().split(" ")
            line_by_term  = ' '.join(line_by_term).split()
            if (len(line_by_term) >= 8):
                iso_G.append(float(line_by_term[5])) # list of G values
                isoBp_minus_isoRp = float(line_by_term[6]) - float(line_by_term[7])
                isoBP_RP.append(isoBp_minus_isoRp)

# plot the lines
def plotAndDist():
    # graphing everything
    plt.gca().invert_yaxis()
    for i in range(0, len(All_G)):
        plt.plot(All_BpRp[i], All_G[i], "-")
    plt.plot(isoBP_RP, iso_G,'r--')
    plt.xlabel("Bp-Rp Values")
    plt.ylabel("G Values")
    plt.show()

# generate an estimate using distances
def distCalc(age_dist_dict, iso_G, isoBP_RP):
    # for each value in iso, check distance to all points of every age. track 2 ages with smallest distances
    for age_value_iso in range (0, len(iso_G)):
        x1 = iso_G[age_value_iso]
        y1 = isoBP_RP[age_value_iso]
        for age in range (0,len(All_G)):
            curr_age_vals_G = All_G[age]
            curr_age_vals_BpRp = All_BpRp[age]
            curr_age = ages[age]
            for point in range (0, len(curr_age_vals_G)):
                x2 = curr_age_vals_G[point]
                y2 = curr_age_vals_BpRp[point]
                distance = calculateDistance(x1, y1, x2, y2)
                age_dist_dict[curr_age] = distance
    return age_dist_dict

# get the actual age
def findApproxAge(age_dist_dict):
    # find the two ages with the smallest distances
    two_ages = dict(sorted(age_dist_dict.items(), key = itemgetter(1))[:2])
    # the actual age must be between these age values
    two_ages_list = []
    for age in two_ages.keys():
        two_ages_list.append(float(age))
    print(two_ages_list)
    predicted_age = sum(two_ages_list)/2
    print("approx age = " + str(predicted_age))

# the main function that runs the other methods
def main(age, G, Bp_Rp, age_dist_dict, iso_G, isoBP_RP):
    # delete the first null values
    All_G.pop(0)
    All_BpRp.pop(0)
    buildGaia(age, G, Bp_Rp)
    buildiso()
    plotAndDist()
    distCalc(age_dist_dict, iso_G, isoBP_RP)
    findApproxAge(age_dist_dict)

# running the program
main(age, G, Bp_Rp, age_dist_dict, iso_G, isoBP_RP)

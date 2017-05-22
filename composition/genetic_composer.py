## 1) Test each sample and assign a fitness score (0.0 - 1.0)
## 2) Select two samples from the population, with more fit samples more likely to be selected.
## 3) Given a certain crossover rate, merge the two samples.
## 4) Return the child sample to a new population pool, part of a new generation.

import random
import notes
import os
import sys


def gen_random_sample(member_size,lowest_note=56,highest_note=80,shortest_note=50,longest_note=600):
    """

    :param member_size: approximate length in time of the sample
    :param lowest_note: lowest possible note in the sample
    :param highest_note: highest possible note in the sample
    :param shortest_note: shortest possible duration of a note (multiple of 50)
    :param longest_note: longest possible duration of a note (multiple of 50)
    :return: a list of (pitch,note) tuples
    """

    # In the future I might generate samples not completely by random, but by having each note be biased
    # towards being closer in pitch to its preceeding note
    # pitches_times = [(random.randint(50,70),random.randint(shortest_note / 50,longest_note / 50) * 50)]
    # member_size -= pitches_times[0][1]
    # prev = 0
    member = []
    while (member_size > 0):
        pitch = random.randint(lowest_note,highest_note)
        time = random.randint(shortest_note / 50,longest_note / 50) * 50
        member.append((pitch,time))
        member_size -= time
    return member


def gen_random_population(population_size,member_size):
    """
    Generate a random population to be used as the seed for genetic improvement.
    :param population_size: The amount of samples in the population
    :param member_size: The length, in seconds (approximately), of each member of the population
    :return: a list of samples
    """
    population = []
    for i in range(0,population_size):
        population.append(gen_random_sample(member_size))

    return population


midi_header = notes.midi_header()
population = gen_random_population(50,5000)
population_file = open('population.txt','w')
sample_num = 0
fitness_file = open('generation0.txt','w')
for sample in population:
    sample_name = 'sample' + "{:04}".format(sample_num) + ".midi"
    sample_num += 1
    midi_file = open(sample_name,'wb')

    track = b''
    track += b'\x00\xb0\x07\x7f'
    ##write controller #7 value = 127

    track += b'\x00\xff\x51\x03\x07\x53\x00'
    ##set tempo to 0x753

    track += b'\x00\xc0\x51'


    for pitch,time in sample:
        track += notes.playNote(pitch,time)

    track += b'\x83\x00\x80\x00\x00'
    track += b'\x00\xff\x2f\x00'

    track_length = notes.toBytes(len(track), 4)
    for b in track_length:
        print ord(b),

    midi_file.write(midi_header)
    midi_file.write(track_length)
    midi_file.write(track)

    midi_file.close()

    os.startfile(sample_name)
    while(True):
        print "Enter the fitness score for the masterpiece you have just listened to: (0 - 100)"
        fitness_score = raw_input()
        try:
            fitness_score = float(fitness_score)
            break
        except:
            print "Please input a floating point number!"

    fitness_file.write(sample_name + "," + str(fitness_score) + "\n")
    population_file.write(sample_name + '\n')


##HOLY CRAP after listening to 50 of these randomly genereated snippets ive realized that I will NOT be able to serve
##as a personal subjective fiteness function
##Maybe I can design a fitness function defined by whether most notes are within a scale, and whether they
##are evenly distibuted throughout time?


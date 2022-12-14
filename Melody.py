    #coding=utf8
    #Version 1.0 By Robin Guo
import PySimpleGUI as sg
import pygame
import random 
import os
from mido import Message,MetaMessage, MidiFile,MidiTrack,bpm2tempo,open_output
from time import sleep
from json import (load as jsonload, dump as jsondump)

SETTINGS_KEYS_TO_ELEMENT_KEYS = {'SPEED':'-BMP-','BEAT_TYPE':'-TYPE-','MAIN_INSTRUMENT':'INSTRUMENT', 'MODE':'CHORD','NOTE_PROGRAM':'Type','CHORD_PROGRAM':'CHORDLIST','BGM':'BackMusic'}
""" ^=rest,-=1/2,==1/8,.=1,..=2,...=3,....=4"""

symbal_to_number = {
        '=': 0.25,
        '-+':0.75,
        '-': 0.5,
        '.+':1.5 ,
        '.':1,
        '..':2,
        '...':3,
        '....':4,
    }

ud2list={'-':['C','D','E','F','G','A','B'],
             'b':['D','E','G','A','B'],
             '#':['C','D','F','G','A']
              }

num2chord = {
        1: 'C',
        2: 'Dm',
        3: 'Em',
        4: 'F',
        5: 'G',
        6: 'Am'
    }

chord2num = {
        'C': 1,
        'Dm': 2,
        'Em': 3,
        'F': 4,
        'G': 5,
        'Am': 6
    }

def List_backmusic(filter,path='.'):
    out=['Default']
    files=os.listdir(path)
    for file in files:
        if file.startswith(filter) and file.endswith('.mid'):
            out.append(file)
    return out

def Note_name2midi_num(note,updown,oct):#oct:1-8
    name2num={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
    ud2num={'#':1,'b':-1,'-':0}
    return (oct+1)*12+name2num[note]+ud2num[updown]

def List_cfg(path='.'):
    out=[]
    files=os.listdir(path)
    for file in files:
        if file.endswith('.ccg'):
            out.append(file)
    return out

def save_cfg(settings_file,values):
    if values:      # if there are stuff specified by another window, fill in those values
        settings={}
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')
                return False

        with open(settings_file, 'w') as f:
            jsondump(settings, f)
        return True
    else:
        return False


def loadcfg(settings_file):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
        return settings
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'Settings file read failed', keep_on_top=True, background_color='red', text_color='white')
        return False


def note(note,velocity = 64, time = 2):
    velocity_modification = randint(-20,20)
    return Message('note_on',note=note,velocity = velocity + velocity_modification, time=time)

def note_off(note,velocity = 64, time=2):
    return Message('note_off',note=note,velocity = velocity, time=time)

def pause():
    sleep(randint(0,100) * .0005)

def notetime(bpminput,duration):
    sleep(60/bpminput*duration)

def Instrument2num(t,argument='Acoustic-Grand-Piano-?????????'):
    switcher = {
        'Acoustic-Grand-Piano-?????????': 0,
        'Bright-AcousticPiano-???????????????': 1,
        'Electric-GrandPiano-?????????': 2,
        'Honky-tonkPiano-????????????': 3,
        'RhodesPiano-??????????????????': 4,
        'ChorusedPiano-???????????????????????????': 5,
        'Harpsichord-????????????(???????????????)': 6,
        'Clavichord-??????????????????(???????????????)': 7,
        'Celesta-?????????': 8,
        'Glockenspiel-??????': 9,
        'Musicbox-?????????': 10,
        'Vibraphone-?????????': 11,
        'Marimba-?????????': 12,
        'Xylophone-??????': 13,
        'TubularBells-??????': 14,
        'Dulcimer-?????????': 15,
        'HammondOrgan-????????????': 16,
        'PercussiveOrgan-???????????????': 17,
        'RockOrgan-????????????': 18,
        'ChurchOrgan-????????????': 19,
        'ReedOrgan-????????????': 20,
        'Accordian-?????????': 21,
        'Harmonica-??????': 22,
        'TangoAccordian-???????????????': 23,
        'Acoustic-Guitar(nylon)-???????????????': 24,
        'Acoustic-Guitar(steel)-????????????': 25,
        'Electric-Guitar(jazz)-???????????????': 26,
        'Electric-Guitar(clean)-???????????????': 27,
        'Electric-Guitar(muted)-???????????????': 28,
        'OverdrivenGuitar-???????????????????????????': 29,
        'DistortionGuitar-???????????????????????????': 30,
        'GuitarHarmonics-????????????': 30,
        'AcousticBass-?????????(????????????)': 32,
        'ElectricBass(finger)-?????????(??????)': 33,
        'Electric-Bass(pick)-?????????(??????)': 34,
        'FretlessBass-????????????': 35,
        'Slap-Bass1-??????Bass-1': 36,
        'Slap-Bass2-??????Bass-2': 37,
        'Synth-Bass1-????????????Bass-1': 38,
        'Synth-Bass2-????????????Bass-2': 39,
        'Violin-?????????': 40,
        'Viola-?????????': 41,
        'Cello-?????????': 42,
        'Contrabass-???????????????': 43,
        'TremoloStrings-?????????????????????': 44,
        'PizzicatoStrings-?????????????????????': 45,
        'OrchestralHarp-??????': 46,
        'Timpani-?????????': 47,
        'String-Ensemble1-??????????????????1': 48,
        'String-Ensemble2-??????????????????2': 49,
        'Synth-Strings1-????????????????????????1': 50,
        'Synth-Strings2-????????????????????????2': 51,
        'ChoirAahs-?????????????????????': 52,
        'VoiceOohs-???????????????': 52,
        'SynthVoice-????????????': 54,
        'OrchestraHit-?????????????????????': 55,
        'Trumpet-??????': 56,
        'Trombone-??????': 57,
        'Tuba-??????': 58,
        'MutedTrumpet-??????????????????': 59,
        'FrenchHorn-?????????(??????)': 60,
        'Brass-Section-?????????(????????????????????????)': 61,
        'Synth-Brass1-??????????????????1': 62,
        'Synth-Brass2-??????????????????2': 63,
        'SopranoSax-??????????????????': 64,
        'AltoSax-?????????????????????': 65,
        'TenorSax-??????????????????': 66,
        'BaritoneSax-??????????????????': 67,
        'Oboe-?????????': 68,
        'EnglishHorn-?????????': 69,
        'Bassoon-??????(??????)': 70,
        'Clarinet-?????????(??????)': 71,
        'Piccolo-??????': 72,
        'Flute-??????': 73,
        'Recorder-??????': 74,
        'PanFlute-??????': 75,
        'BottleBlow-??????': 76,
        'Shakuhachi-????????????': 77,
        'Whistle-?????????': 78,
        'Ocarina-????????????': 79,
        'Lead-1(square)-????????????1(??????)': 80,
        'Lead-2(sawtooth)-????????????2(?????????)': 81,
        'Lead-3-(caliopelead)-????????????3': 82,
        'Lead-4-(chifflead)-????????????4': 83,
        'Lead-5(charang)-????????????5': 84,
        'Lead-6(voice)-????????????6(??????)': 85,
        'Lead-7(fifths)-????????????7(????????????)': 86,
        'Lead-8-(bass+lead)????????????8(???????????????)': 87,
        'Pad-1-(newage)-????????????1(?????????)': 88,
        'Pad-2(warm)-????????????2-(??????)': 89,
        'Pad-3(polysynth)-????????????3': 90,
        'Pad-4(choir)-????????????4-(??????)': 91,
        'Pad-5(bowed)-????????????5': 92,
        'Pad-6(metallic)-????????????6-(?????????)': 93,
        'Pad-7(halo)-????????????7-(??????)': 94,
        'Pad-8(sweep)-????????????8': 95,
        'Sitar-?????????(??????)': 104,
        'Banjo-?????????(??????)': 105,
        'Shamisen-?????????(??????)': 106,
        'Koto-????????????(??????)': 107,
        'Kalimba-?????????': 108,
        'Bagpipe-??????': 109,
        'Fiddle-????????????': 110,
        'Shanai-??????': 111

    }

        # get() method of dictionary data type returns
        # value of passed argument if it is present
        # in dictionary otherwise second argument will
        # be assigned as default value of passed argument
    if t==1:
        return switcher
    else:
        return switcher.get(argument, 0)


def playrythem(segtime,bpm):
    outport = open_output('Microsoft GS Wavetable Synth 0')
    seglist=segtime.split('|')
    for oneseg in seglist:
        if len(oneseg)!=0:
            notestr=oneseg.split(' ')
            for seg in notestr:
                outport.send(Message('note_on',channel=9,note=37,velocity = 127, time=0))
                notetime(bpm,symbal_to_number.get(seg,0))
    outport.close()

def segment_rythem (numerator):
    segtimeseq=[]
    outstr=''
    segbeat=numerator
    tempt=[]
    if segbeat>3:
        timechoice=['.','=','-+','-','.+','..','...','....'] #1/4,1/2/1/2/3/4 beat
        timereal=[1,0.25,0.75,0.5,1.5,2,3,4]
        endstr='....'
    else:
        timechoice = ['.','=','-+','-', '.+', '..', '...']  # 1/4,1/2/1/2/3 beat
        timereal = [1,0.25,0.75,0.5, 1.5, 2, 3]
        endstr='...'
    for i in range(4):
        segbeat = numerator
        while segbeat>0:
                if i<3 :
                    t=random.randint(0,len(timereal)-4) #????????????????????????
                else:
                    t = random.randint(0, len(timereal) - 1)

                if timereal[t] in [1.5] and not probability(0.25):
                    continue
                if timereal[t] in [0.75,0.25] and not probability(0.1):
                    continue
                segbeat=segbeat-timereal[t]

                if segbeat<0:   #??????????????????????????????????????????????????????????????????
                    segbeat=segbeat+timereal[t]
                    continue
                if segbeat>=0:  #???????????????????????????????????????????????????????????????

                    segtimeseq.append(timechoice[t])

                    if timereal[t] in [0.5,1.5] and segbeat>=0.5:  #???????????????????????????????????????????????????????????????????????????????????????
                        segbeat=segbeat-0.5
                        segtimeseq.append('-')
                        continue

                    if timereal[t] == 0.75 and segbeat >= 0.25:
                        segbeat = segbeat - 0.25
                        segtimeseq.append('=')
                        continue

                    if timereal[t] ==0.25 and segbeat>=0.75:  #???????????????????????????????????????????????????????????????????????????????????????
                        segbeat=segbeat-0.75
                        segtimeseq.append('=')
                        if probability(0.5):
                            segtimeseq.append('=')
                            segtimeseq.append('=')
                        else:
                            segtimeseq.append('-')
                        continue

        singlestr=' '.join(segtimeseq)
        tempt.append(singlestr)
        segtimeseq.clear()

    for str in tempt[0:4]:
        outstr = outstr + str + '|'
    outstr = outstr +'\n'
    for str in tempt[0:3]:
        outstr = outstr + str + '|'
    outstr=outstr+endstr+'|'
    return outstr

def probability(req):
    a=random.random()
    if a <=req:
        return True
    else:
        return False

def segment_chords(mode):

    majors=['C|G|Am|F|C|G|Am|F|','C|G|Am|G|F|C|F|G|','C|G|Am|G|F|C|Dm|G|','C|G|Am|G|F|Em|F|G|','C|G|Am|G|F|Em|Dm|G|'
            ,'C|G|Am|Em|F|C|F|G|','C|G|Am|Em|F|C|Dm|G|','C|G|Am|Em|F|Em|F|G|','C|G|Am|Em|F|Em|Dm|G|',
            'C|G|Am|C|F|C|F|G|','C|G|Am|C|F|C|Dm|G|','C|G|Am|C|F|Em|F|G|','C|G|Am|C|F|Em|Dm|G|','F|G|Em|Am|F|G|C|C|','F|G|Em|Am|Dm|G|C|C|',
            'C|G|Am|Em|F|G|C|C|','C|F|C|G|C|F|C|G|']
    minors=['Am|Em|F|C|Dm|Am|Dm|E|','Am|Em|F|C|Dm|Am|F|G|','Dm|G|C|F|G|E|Am|','Am|G|C|F|G|E|Am|','Am|Em|F|C|Dm|E|Am|Am|',
            'Am|G|F|Em|Dm|C|Dm|Em|','Am|G|F|Em|Dm|C|F|Em|','Am|C|F|G|Am|C|F|G|','Am|F|C|G|Am|F|C|G|','Am|Dm|Am|Em|Am|Dm|Am|Em|','C|G|Am|Em|F|G|Am|Am|']

    if mode=='Major':
        mainchord='C'
        outchords = majors[random.randint(1, len(majors) - 1)]
    else:
        mainchord='Am'
        outchords = minors[random.randint(1, len(minors) - 1)]
    return outchords

def check_pattern(pattern):
    pattern = pattern.replace('\n', '')
    pattern4check = pattern.replace('^', '')
    rythem = pattern4check.split('|')

    if rythem[-1] == '':
        rythem.pop()
    for i,segs in enumerate(rythem):
        seg=segs.split(' ')
        for j,note in enumerate(seg):
            if note not in list(symbal_to_number.keys()):
                return 'In Segment '+str(i+1)+',( '+note+' ) is undefined'
                break
    return   pattern.split('|')

def check_chords(progress):
    songseqs = progress.replace('\n', '')
    songs = songseqs.split('|')  # chordsequence,1 Chord per segment
    if songs[-1] == '':
        songs.pop()  # del last ???|???
    for i,segs in enumerate(songs):
        chords=segs.split(' ')
        for j,chord in enumerate(chords):
            if chord not in list(chord2num.keys()):
                return 'In Segment '+str(i+1)+',( '+chord+' ) is undefined'
                break
    return   songs

def create_midi(speed,nu,rythemstr,songseqs,key,outfile,instru,backmusic='Default',ticksPerbeat=96): #(??????bpm????????????3or4???????????????????????????????????????????????????????????????????????????)
#???????????????
#??????????????????????????????????????????????????????
#???????????????????????????????????????????????????????????????????????????????????????
    mid = MidiFile()
    mid.ticks_per_beat=ticksPerbeat
    track0 = MidiTrack()
    melodytrack= MidiTrack()


    mid.tracks.append(track0)
    mid.tracks.append(melodytrack)

    #mid.tracks.append(drumtrack)
    bpm = speed
    tempo = bpm2tempo(bpm)
    track0.append(MetaMessage('time_signature', numerator=nu, denominator=4))
    track0.append(MetaMessage('set_tempo', tempo = tempo, time=0))
    melodytrack.append(Message('program_change',channel=1, program=instru, time=0))
    notelist=[key,key+2,key+4,key+5,key-5,key-3] # C,D,E,F,G,A
    majorchord=[-5,0,4,7,12]
    minorchord=[-5,0,3,7,12]
    # rythemstr=rythemstr.replace('\n','')
    # rythem=rythemstr.split('|')
    # if rythem[-1]=='':
    #     rythem.pop()
    rythem=check_pattern(rythemstr)
    if isinstance(rythem,str):
        sg.popup(rythem, keep_on_top=True)
        return False
    songs=check_chords(songseqs)
    if isinstance(songs, str):
        sg.popup(songs, keep_on_top=True)
        return False
    melodytrack.append(Message('note_on',channel=1, note=60, velocity=0, time=0))
    melodytrack.append(Message('note_off',channel=1, note=60, velocity=0, time=int(ticksPerbeat*(2*nu-1))))
    #beatstart=True
    middlenote=0
    lastnote=0
    for i,chord in enumerate(songs):
        segtime = rythem[i]
        st = segtime.split(' ')
        schord=chord.split(' ')
         #???????????????????????????
        cnotelist = []
        for singlechord in schord:
            cnotelist.append(chord2num.get(singlechord,0))

        sumofnotetime = 0
        for j,t in enumerate(st):#??????


            if '^' in t:
                velo=0
                t=t.replace('^','')
            else:
                velo = random.randint(108, 127)
            note=symbal_to_number.get(t,0) #???????????????????????? .~1
            if note==0:
                sg.popup(t+" can not be recongnized!", keep_on_top=True)
                return False
            sumofnotetime=sumofnotetime+note
            rt=int(note*ticksPerbeat)  #??????????????????msg-time 1~96


            if len(cnotelist)>1 and sumofnotetime>nu//2 and j>0:
                cnote=cnotelist[1]
            else:
                cnote=cnotelist[0]

                # ???????????????????????????
            if (i == len(songs) - 1) and (j == len(st) - 1) and sumofnotetime > nu // 2:
                n = notelist[cnote - 1]
            # ????????????????????????
            elif lastnote==0:
                ran = random.randint(0, 4)
                if cnote in [1, 4, 5]:
                    n = notelist[cnote - 1] + majorchord[ran]
                else:
                    n = notelist[cnote - 1] + minorchord[ran]
                if n % 12 in [0, 5]:  # ??????????????? C or F,??????AB???DE
                    melodytrack.append(Message('note_on', channel=1, note=n - 3, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 3, velocity=0, time=int(ticksPerbeat * 0.5)))
                    melodytrack.append(Message('note_on', channel=1, note=n - 1, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 1, velocity=0, time=int(ticksPerbeat * 0.5)))
                elif n % 12 in [2, 7]:  # ??????????????? D or G,??????BC???EF
                    melodytrack.append(Message('note_on', channel=1, note=n - 3, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 3, velocity=0, time=int(ticksPerbeat * 0.5)))
                    melodytrack.append(Message('note_on', channel=1, note=n - 2, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 2, velocity=0, time=int(ticksPerbeat * 0.5)))
                else:  # ??????????????? E or A,??????CD???FG
                    melodytrack.append(Message('note_on', channel=1, note=n - 4, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 4, velocity=0, time=int(ticksPerbeat * 0.5)))
                    melodytrack.append(Message('note_on', channel=1, note=n - 2, velocity=velo, time=0))
                    melodytrack.append(
                        Message('note_off', channel=1, note=n - 2, velocity=0, time=int(ticksPerbeat * 0.5)))
                if velo!=0:
                    velo = 127

            else:

                while True:
                    ran = random.randint(0, 4)
                    if cnote in [1, 4, 5]:
                        n = notelist[cnote - 1] + majorchord[ran] # ???????????????????????????   majorchord=[-5,0,4,7]
                    else:
                        n = notelist[cnote - 1] + minorchord[ran]
                    if abs(n - lastnote) < 11:
                        break

            #???????????????????????????
            if middlenote>0 :
                if lastnote < n:
                    # E
                    if lastnote % 12 in [4,11]:
                        note = lastnote + 1
                    else:
                        note = lastnote + 2
                else:
                    # C,F
                    if lastnote % 12 in [0, 5]:
                        note = lastnote - 1
                    else:
                        note = lastnote - 2
                # ????????????????????????
                melodytrack.append(Message('note_on', channel=1, note=note, velocity=velo, time=0))
                melodytrack.append(Message('note_off', channel=1, note=note, velocity=velo, time=middlenote))

                # ??????????????????
                melodytrack.append(Message('note_on', channel=1, note=n, velocity=velo, time=0))
                melodytrack.append(Message('note_off', channel=1, note=n, velocity=velo, time=rt))

                middlenote = 0

            else:
                #?????????????????????????????????
                #ran = random.randint(1, 8)
                if rt <= ticksPerbeat and probability(0.5) and lastnote!=0 and velo!=0:
                    middlenote = rt
                else:
                    melodytrack.append(Message('note_on', channel=1, note=n, velocity=velo, time=0))
                    melodytrack.append(Message('note_off', channel=1, note=n, velocity=velo, time=rt))

            lastnote = n




#????????????
    if backmusic=='Default':
#Chordstrack
        chordstrack=MidiTrack()
        mid.tracks.append(chordstrack)
        chordstrack.append(Message('program_change', channel=2,program=0, time=0))
        chordstrack.append(Message('note_on',channel=2, note=60, velocity=0, time=0))
        chordstrack.append(Message('note_off',channel=2, note=60, velocity=0, time=int(ticksPerbeat*2*nu)))
        for index in range(len(songs)):
            cnote=chord2num.get(songs[index],0)
            if cnote in [1,4,5]:
                n1=notelist[cnote-1]
                n2=notelist[cnote-1]+majorchord[2]
                n3=notelist[cnote-1]+majorchord[3]
            else:
                n1=notelist[cnote-1]
                n2=notelist[cnote-1]+minorchord[2]
                n3=notelist[cnote-1]+minorchord[3]

            for j in range(nu):
                chordstrack.append(Message('note_on',channel=2, note=n1, velocity=48, time=0))
                chordstrack.append(Message('note_on',channel=2, note=n2, velocity=48, time=0))
                chordstrack.append(Message('note_on',channel=2, note=n3, velocity=48, time=0))
                chordstrack.append(Message('note_off',channel=2, note=n1, velocity=0, time=ticksPerbeat))
                chordstrack.append(Message('note_off',channel=2, note=n2, velocity=0, time=0))
                chordstrack.append(Message('note_off',channel=2, note=n3, velocity=0, time=0))
    #drumtrack
        drumtrack=MidiTrack()
        mid.tracks.append(drumtrack)
        drumtrack.append(Message('program_change', channel=9, time=0))
        for i in range(len(rythem)+2):
            drumtrack.append(Message('note_on',channel=9, note=35, velocity=64, time=0))
            drumtrack.append(Message('note_off',channel=9, note=35, velocity=0, time=ticksPerbeat))
            for j in range(nu-1):
                drumtrack.append(Message('note_on',channel=9, note=39, velocity=48, time=0))
                drumtrack.append(Message('note_off',channel=9, note=39, velocity=0, time=ticksPerbeat))
    else:
        #backmusic = MidiFile('back-4-Simple.mid')
        backmusic = MidiFile(backmusic)
        bmchordlist=[]#?????????????????????????????????????????????????????????key???????????????value???msg?????????
        seglast=nu*ticksPerbeat
        justment2c = key % 12
        if justment2c > 5:
            justment2c = justment2c - 12
        for track in backmusic.tracks[1:]:#
            timelast=0 #????????????time????????????????????????????????????nu*ticksPerbeat
            tracktemptlist={'drum':[],'C':[],'Dm':[],'Em':[],'F':[],'G':[],'Am':[],'trackhead':[]}
            for msg in track:#???????????????????????????
                if msg.type in ['track_name','program_change']:
                    tracktemptlist['trackhead'].append(msg)
                elif msg.type in ['end_of_track']:
                    break
                else:
                    if msg.time!=0 :
                        timelast=timelast+msg.time
                    firstime = timelast % seglast #??????????????????
                    segnum = timelast // seglast  #?????????????????????????????????????????? ???drum_only,C,Dm,Em,F,G,Am??????
                    if len(tracktemptlist[num2chord.get(segnum,'drum')])==0: #?????????????????????????????????????????????
                        msg.time=firstime
                    if msg.channel != 9:
                        try:
                            msg.note = msg.note + justment2c
                        except Exception as e:
                            # print(msg)
                            pass
                    tracktemptlist[num2chord.get(segnum,'drum')].append(msg)
            bmchordlist.append(tracktemptlist)

        for i,subtrack in enumerate(bmchordlist):
            backtrack=MidiTrack()
            for msg in subtrack['trackhead']:
                backtrack.append(msg)
            timelast = 0

            for j in range(0,2):
                if i == 0:
                    for msg in subtrack['drum']:

                        backtrack.append(msg)
                        timelast=timelast+msg.time

                backtrack.append(Message('note_on',channel=9, note=39, velocity=0, time=nu*ticksPerbeat-timelast))
                timelast = 0 #??????????????????
            for chords in songs:
                chord1seg = chords.split(' ')
                chordnum = len(chord1seg)
                stime=(nu * ticksPerbeat) // chordnum
                for chord in chord1seg:
                    for msg in subtrack[chord]:

                        timelast = timelast + msg.time
                        if timelast<stime:

                            backtrack.append(msg)
                        else:
                            timelast = timelast-msg.time
                            break
                    backtrack.append(Message('note_on', channel=9, note=39, velocity=0,time=stime - timelast))
                    timelast = 0  # ??????????????????
            mid.tracks.append(backtrack)
    mid.save(outfile)
#    sg.popup("DONE!", keep_on_top=True)
    return create_midi

# def playMIDI9 (inputFile):#???????????????????????????????????????
#     for msg in MidiFile(inputFile).play():
#         outport.send(msg)


def playMIDI (inputFile):

    freq = 44100
    bitsize = -16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq, bitsize, channels, buffer)#?????????
#    pygame.mixer.music.load('./'+'checkout.mid'+'.mid')
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(inputFile)
        pygame.mixer.music.play(loops = -1)
    else:
        pygame.mixer.music.stop()

    return pygame.mixer.music.get_busy()


def CheckMIDI (MIDIfile):
    if MIDIfile.endswith('.mid'):
        checkmid = MidiFile(MIDIfile)
        print(checkmid)
    #print('--------------------------------------')
    # for i, track in enumerate(checkmid.tracks):#enumerate()???????????????????????????????????????0
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:#???????????????????????????
    #         print(msg)
    return CheckMIDI

def Collapsible(layout, key, collapsed=False):
    """
    User Defined Element
    A "collapsable section" element. Like a container element that can be collapsed and brought back
    :param layout:Tuple[List[sg.Element]]: The layout for the section
    :param key:Any: Key used to make this section visible / invisible
    :param title:str: Title to show next to arrow
    :param arrows:Tuple[str, str]: The strings to use to show the section is (Open, Closed).
    :param collapsed:bool: If True, then the section begins in a collapsed state
    :return:sg.Column: Column including the arrows, title and the layout that is pinned
    """
    return sg.Column([[sg.pin(sg.Column(layout, key=key, visible=not collapsed))]], pad=(0,0))

def make_window(theme=None):
    sg.theme(theme)
    menu_def = [['&File',['Export MIDI File','E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Export MIDI File', 'Versions','Exit']]
    graph_right_click_menu_def = [[], ['Erase','Draw Line', 'Draw',['Circle', 'Rectangle', 'Image'], 'Exit']]
    input_layout =  [
                # [sg.Menu(menu_def, key='-MENU-')],

                [sg.Button('Save to'),sg.Input(s=(10),key='Cfgfile'),
                 sg.Combo(List_cfg(), default_value='Default.ccg', s=(12, 22), enable_events=True,
                                 readonly=True, k='cfg'),sg.Button('Load')],

                [sg.Text('Bpm'),sg.Spin([i for i in range(30,190)], initial_value=120, k='-BMP-'),
                 sg.Text('Numerator'),sg.Combo([3,4], enable_events=True,default_value=4, k='-TYPE-'),
                 sg.Text('Mode'),sg.Combo(['Major', 'Minor'],default_value='Major', k='CHORD'),sg.Text('1='),sg.Combo(['-','#','b'],default_value='-',key='#b',enable_events=True),sg.Combo(['C','D','E','F','G','A','B'],key='note',default_value='C'),

                 sg.Combo(list(range(2,9)),default_value='6',key='oct'),
                 sg.Text('Instrument'),sg.Combo(list(Instrument2num(1).keys()), default_value='Flute-??????', k='INSTRUMENT')],
                [sg.Text('"^":rest|"=":0.25|"-":0.5|"-+":0.75|".-"=1.5|".":1|"..":2|"...":3|"....":4',background_color='yellow',justification='center',font='Amethyst 18',s=100)],
                [sg.Text('Notes Patten',justification='right',s=12),sg.Multiline('- - - - ..|- - - - ..|.+ - .+ -|- - - - ..|\n- - - - ..|- - - - ..|.+ - .+ -|....|',
                 font='Amethyst 24',size=(66,2),key='Type'),sg.Button('???'),sg.Button('+Randowm',key='Random'),sg.Button('Clear')],#??????????????????

                [sg.Text('Chords Progress',justification='right',s=12),sg.Multiline('C G|Am|Dm|G|C|Am|G|C|',font='Elephant 24',size=(36,2),key='CHORDLIST'),
                 sg.Text('Accompaniment'), sg.Combo(List_backmusic('back-4'),default_value='Default',s=(15,22), enable_events=True, readonly=True, k='BackMusic')], #????????????

                [sg.Button('Create'),sg.Button('Play',button_color='yellow on green',disabled=True)]
                ]
#                [sg.Text('Anything that requires user-input is in this tab!')],
#                [sg.Slider(orientation='h', key='-SKIDER-'),
#                 sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'),],
#                [sg.Checkbox('Checkbox', default=True, k='-CB-')],
#                [sg.Radio('Radio1', "RadioDemo", default=True, size=(10,1), k='-R1-'), sg.Radio('Radio2', "RadioDemo", default=True, size=(10,1), k='-R2-')],
#                [sg.Combo(values=('Combo 1', 'Combo 2', 'Combo 3'), default_value='Combo 1', readonly=False, k='INSTRUMENT')]]
#                 sg.OptionMenu(values=('Option 1', 'Option 2', 'Option 3'),default_value='Option 3',  k='-OPTION MENU-'),],
#                [sg.Spin([i for i in range(1,11)], initial_value=10, k='-SPIN-'), sg.Text('Spin')],
#                [sg.Multiline('Demo of a Multi-Line Text Element!\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', size=(45,5), expand_x=True, expand_y=True, k='-MLINE-')],
#                [sg.Button('Button'), sg.Button('Popup'), sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGO-')]]


    analysis_layout = [[sg.Text("Choose MIDI file",key='MDISPLAY')],
                    [sg.Button("Open file"),sg.Button('Play',button_color='yellow on green',disabled=True,key='PlayMusic'),sg.Button('Empty')],
                    [sg.Multiline(key='contents',size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                     reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True,visible=False)]]

    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values = sg.theme_list(),
                      size =(20, 4),
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]

    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)]]
    layout +=[[sg.TabGroup([[  sg.Tab('Creation', input_layout),
                               sg.Tab('Files', analysis_layout),
                               sg.Tab('Theme', theme_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),
               ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Auto Melody Creation', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)

    return window


def main():
    window = make_window(sg.theme())
    event, values = window.read(timeout=100)
    default_numerate = values['-TYPE-']
    # This is an Event Loop

    while True:
        event, values = window.read(timeout=100)

        if event in (None, 'Exit'):
            break
        #input_layout
        if event=='Export MIDI File':
            folder_or_file = sg.popup_get_file('Select MID File', keep_on_top=True,file_types=(("Mid Files", "*.mid"),),default_extension='mid',save_as=True)
            path=str(folder_or_file)
            if path not in ['None', '']:
                path=path.replace("/","\\")
                os.system('copy checkout.mid '+ path)

        elif event=='Save to':
            if values['Cfgfile']=='':
                sg.popup('Please input you config name!',keep_on_top=True)
            else:
                path = values['Cfgfile']+'.ccg'
                if path not in ['None', '']:
                    if os.path.exists(path) :
                        if sg.popup_yes_no('File exist,Want to overwrite?', keep_on_top=True) == 'Yes':

                            if save_cfg(path, values):
                                sg.popup('Parameters saved', keep_on_top=True)
                            else:
                                sg.popup('Parameters save failed', keep_on_top=True)
                            window['cfg'].update(values=List_cfg(),set_to_index=0)
                    else:
                        if save_cfg(path, values):
                            sg.popup('Parameters saved', keep_on_top=True)
                        else:
                            sg.popup('Parameters save failed', keep_on_top=True)
                        window['cfg'].update(values=List_cfg(), set_to_index=0)

        elif event=='Save as':
            folder_or_file = sg.popup_get_file('Select Config File', keep_on_top=True,file_types=(("Config Files", "*.ccg"),), default_extension='ccg',save_as=True)
            path = str(folder_or_file)
            if path not in ['None', '']:
                if save_cfg(path,values):
                    sg.popup('Parameters saved', keep_on_top=True)
                else:
                    sg.popup('Parameters save failed', keep_on_top=True)
            window['cfg'].update(List_cfg())


        elif event=='Load':
            settings=loadcfg(values['cfg'])
            for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
                try:
                    window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
                except Exception as e:
                    print(f'Problem updating PySimpleGUI window from settings. Key = {key}')
        elif event == 'About':
            sg.popup('MELODY TOOLS',
                     'by Robin Guo',
                     'robin_guo@live.cn', keep_on_top=True)
        elif event == '-TYPE-':

            if default_numerate!=values['-TYPE-']:
                sg.popup("Numerate is changed!\nAll Contents will be Cleared!", keep_on_top=True)
                window['BackMusic'].update(values=List_backmusic('back-'+ str(values['-TYPE-'])), set_to_index=0)

                window["Type"]('')
                window["CHORDLIST"]('')
                # window["SEGTEMP"]('')
                window["CHORD"]('')
                default_numerate = values['-TYPE-']
        elif event=='#b':
            window['note'].update(values=ud2list[values['#b']],set_to_index=0)

        elif event == 'Random':
            window["Type"](values["Type"]+'\n'+segment_rythem(values['-TYPE-']))
            window["CHORDLIST"](values["CHORDLIST"]+'\n'+segment_chords(values['CHORD']))
            # playrythem(segment_rythem(values['-TYPE-']),values['-BMP-'])
        # elif event == '+':
        #     window["Type"](values['Type'] + values['SEGTEMP'] + '|')
        #     window["CHORDLIST"](values['CHORDLIST'] + str(values['CHORD']) + '|')
        elif event == 'Clear':
            window["Type"]('')
            window["CHORDLIST"]('')
        elif event == '???':
            playrythem(values['Type'], values['-BMP-'])
        elif event == 'Create':
            # create_midi(speed,nu,rythemstr,songseqs,key,outfile,instru)
            if create_midi(values['-BMP-'], values['-TYPE-'], values['Type'], values['CHORDLIST'], Note_name2midi_num(values['note'],values['#b'],values['oct']),
                        'checkout.mid', Instrument2num(2,values['INSTRUMENT']), values['BackMusic']):

                window['Play'].update(disabled=False)
                window["Play"]('Play')
                toggleplay = False
                if playMIDI('checkout.mid'):
                    window['Create'].update(disabled=True)
                    window["Play"]('Stop')
                else:
                    window['Create'].update(disabled=False)
                    window["Play"]('Play')
        elif event == 'Play':
            if playMIDI('checkout.mid'):
                window['Create'].update(disabled=True)
                window["Play"]('Stop')

            else:
                window['Create'].update(disabled=False)
                window["Play"]('Play')

        #analysis_layout
        elif event == "Open file":
            folder_or_file = sg.popup_get_file('Choose MIDI file', keep_on_top=True)
            if str(folder_or_file) not in ['None','']:
                CheckMIDI(str(folder_or_file))
                window["MDISPLAY"](str(folder_or_file))
                window['contents'].update(visible=True)
                window['PlayMusic'].update(disabled=False)
                playMIDI(str(folder_or_file))
                window["PlayMusic"]('Stop')
        elif event == 'PlayMusic':
            if playMIDI(str(folder_or_file)):
               window["PlayMusic"]('Stop')
            else:
               window["PlayMusic"]('Play')
        elif event == "Empty":
            window["MDISPLAY"]("Choose MIDI file")
            window['contents']('')
            window['contents'].update(visible=False)
        #Theme_layout
        elif event == "Set Theme":
            print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)

    window.close()
    exit(0)

if __name__ == '__main__':
    sg.theme('Lightgreen10')
#    sg.theme('dark red')
#    sg.theme('dark green 7')
    # sg.theme('DefaultNoMoreNagging')
    main()
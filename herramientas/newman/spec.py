# Cada trozo: id, archivo, párrafos (lista; una sublista = párrafos que se unen en uno)
import re
def P(f):
    return [x.strip() for x in open('/home/claude/newman/pulido/' + f).read().split('\n\n') if x.strip()]

FIX = [
    ('beneath’ Him', 'beneath Him'), ('sparrows’ He determined', 'sparrows.’ He determined'), ('But 28s He has', 'But He has'), ('\\\\ 7 HEN our Lord came upon ‘* earth', 'WHEN our Lord came upon earth'),
    ('thy son’ and to him, ‘Behold thy Mother’ we', 'thy son,’ and to him, ‘Behold thy Mother,’ we'), ('for 2 go MEDITATIONS AND INTERCESSIONS those', 'for those'),
    ('Lord not only offered ^ Himself', 'OUR Lord not only offered Himself'), ('appearance ot mere', 'appearance of mere'), ('heavenly kingdom.1', 'heavenly kingdom.'),
    ('Name Jesus’ But', 'Name Jesus.’ But'), ('says, foretelling His coming, A child', 'says, foretelling His coming, ‘A child'), ('Peace ‘(Isaias', 'Peace’ (Isaias'), ('Thou earnest', 'Thou camest'),
    ('announced before He came, 4 Behold I create new heavens and a new earth1', 'announced before He came, ‘Behold I create new heavens and a new earth’'), ('calls Him 4 The image', 'calls Him ‘The image'),
    ('calls Him 4 the Amen', 'calls Him ‘the Amen'), ('creation of God 1 (', 'creation of God’ ('), ('husbands to 280 meditations and intercessions be', 'husbands to be'),
    ('‘ I "\'HE inspired', 'THE inspired'), ('He shall- save', 'He shall save'), ('sins ’ (Matt. L 21)', 'sins’ (Matt. i. 21)'), ('except that U He desired', 'except that He desired'),
    ('salvation’ Hence', 'salvation? Hence'), ('was lost ’ (Matt. xvii. 1 1,', 'was lost’ (Matt. xviii. 11,'), ('all sinners,$', 'all sinners.'), ('good works’ look', 'good works,’ look'),
    ('OT. PAUL tells us to ‘look on ^ Jesus', 'ST. PAUL tells us to ‘look on Jesus'), ('wre are', 'we are'), ('If thou 262 MEDITATIONS and intercessions canst', 'If thou canst'), ('believeth ’ (Mark, ix. 22^23)', 'believeth’ (Mark ix. 22-23)'),
    ('faith ’ (Luke', 'faith’ (Luke'), ('charit)', 'charity'), ('they do’ Teach', 'they do.’ Teach'), ('A MONG', 'AMONG'), ('conquer ‘(Apoc', 'conquer’ (Apoc'), ('4 1 saw heaven', '‘I saw heaven'),
    ('fight ’ (Apoc. xix. 1 1)', 'fight’ (Apoc. xix. 11)'), ('clean ’ (verse T 13)', 'clean’ (verse 13)'), ('Lamb ’ (Apoc', 'Lamb’ (Apoc'), ('•meekness', 'meekness'), ('wonderfully ’ (Psalm', 'wonderfully’ (Psalm'),
    ('tipon', 'upon'), ('they t 2 may', 'they may'), ('Himself ‘(John', 'Himself’ (John'), ('St John', 'St. John'), ('Father* (John', 'Father’ (John'), ('everlasting ’ (John', 'everlasting’ (John'),
    ('Father of all* (Eph', 'Father of all’ (Eph'), ('Iloly', 'Holy'), ('Almighty’ and then', 'Almighty,’ and then'), ('He Himself, says', 'He Himself says'),
    ('"DEHOLD the Lamb of God, ^ behold Him who takcth', '‘BEHOLD the Lamb of God, behold Him who taketh'), ('sins of the world. So spoke', 'sins of the world.’ So spoke'), ('a lamb S without', 'a lamb without'),
    ('shearers ’ (', 'shearers’ ('), ('we arc healed ’(', 'we are healed’ ('), ('slain; ’ and', 'slain;’ and'), ('the Lamb/...', 'the Lamb’...'), ('saying, 4 Thou', 'saying, ‘Thou'), ('nation ’ (', 'nation’ ('),
    ('benediction ’ (', 'benediction’ ('), ('co?iverted', 'converted'), ('hour after s 2 hour', 'hour after hour'), ('Father, etc.', 'Father, etc.'),
    ('I. T T IS bodily pains were 1 A greater', '1. HIS bodily pains were greater'), ('has a, soul', 'has a soul'), ('other animal,$', 'other animal.'), ('seem to. suffer', 'seem to suffer'), ('c*nd all', 'and all'),
    ('death: 4 My soul is sorrowful even unto death’ The', 'death: ‘My soul is sorrowful even unto death.’ The'), ('allnoble, all-generous, ail-tender, allpure', 'all-noble, all-generous, all-tender, all-pure'),
    ('I. T T is over pow, O Lord, as A with', '1. IT is over now, O Lord, as with'), ('we havp professed', 'we have professed'), ('cons urn matum est', 'consummatum est'),
    ('the prophet H is coming', 'the prophet His coming'), ('nativity and F f 2 all', 'nativity and all'), ('Angels?* —', 'Angels?’ —'), ('orphans.* He', 'orphans.’ He'), ('friends.* He', 'friends.’ He'),
    ('little ones,* and', 'little ones,’ and'), ('‘With desire’ He says', '‘With desire,’ He says'), ('before I suffer’ Thus', 'before I suffer.’ Thus'), ('death; ’', 'death;’'), ('forsaken Me? ’', 'forsaken Me?’'),
    ('Oratoiy', 'Oratory'), ('is- lost', 'is lost'), ('seems • never', 'seems never'), ('Thy infant Lord— as Thou didst hang', 'thy infant Lord — as thou didst hang'), ('as Thou wast found', 'as thou wast found'),
    ('not.* Then', 'not.’ Then'), ('St Elizabeth', 'St. Elizabeth'), ('tha,n', 'than'), ('‘laudabilis numerus ’', '‘laudabilis numerus’'), ('Abraham Who', 'Abraham who'), ('a$ Isaias', 'as Isaias'),
    ('beginningof it — thoudidst', 'beginning of it — thou didst'), ('ii. The blessed', '11. The blessed'), ('HOPE!N GOD— REDEEMER 425 ', ''), ('business; 1 and', 'business;’ and'),
    ('thee? ’ —', 'thee?’ —'), ('made.no', 'made no'), ('1 2. I see', '12. I see'), ('Ho\\V', 'How'), ('sortie peril F F or', 'some peril or'), ('in in heaven', 'in heaven'),
    ('1 5. He', '15. He'), ('1 6. He', '16. He'),
    ('OUR LORD REFUSES SYMPATHY i. O YMPATHY may be called ^ an', '1. SYMPATHY may be called an'), ('rathertranscendentally', 'rather transcendentally'), ('created 4 can add', 'created can add'),
    ('feach', 'each'), ('otie', 'one'), ('rny duty', 'my duty'), ('began 41 8 ON CHRISTIAN DOCTRINE to sound', 'began to sound'), ('St Joseph', 'St. Joseph'), ('Me? ‘Thus', 'Me?’ Thus'),
    ('of man be free', 'of man, be free'), ('in the. old', 'in the old'), ('4 1 know you not’', '‘I know you not,’'), ('thee? ‘It was', 'thee?’ It was'), ('O woman? ’', 'O woman?’'), ('the Host O my', 'the Host. O my'),
    ('A FTER all His discourses ***• were', 'AFTER all His discourses were'), ('waste? 1 —', 'waste?’ —'), ('followers..', 'followers.'), ('His servant A heathen', 'His servant. A heathen'),
    ('Brute! ’', 'Brute!’'), ('sweeti most', 'sweet, most'), ('against E E the Face', 'against the Face'), ('‘ thou art the man’', '‘Thou art the man.’'), ('do so.* Yfes', 'do so.’ Yes'),
    ('acknowledgEE2 pient', 'acknowledgment'), ('hcec', 'hæc'), ('deserve Thy pity', 'deserve thy pity'),
    ('22 2 SHORT MEDITATIONS ON THE ', ''), ('246 THE STATIONS OF THE CROSS ', ''), ('day 4 They shall look on Him whom they pierced 1;', 'day ‘They shall look on Him whom they pierced’;'),
    ('person’ and threw', 'person,’ and threw'), ('Thou are judged', 'Thou art judged'), ('savehim', 'save him'), ('to it The sanctity', 'to it. The sanctity'),
    ('OATAN had a second fall, when ^ our', 'SATAN had a second fall, when our'), ('T ^ VER since the prophecy ot ^ old time', 'EVER since the prophecy of old time'),
    ('OATAN will have a third and ^ final', 'SATAN will have a third and final'), ('awful r 2 humiliation', 'awful humiliation'), ('the Evil One$', 'the Evil One.'),
    ('‘/^ONSUMMATUM est’ It', '‘Consummatum est.’ It'), ('buryingclothes', 'burying-clothes'), ('rejoice in ^ the glory of the same Holy Cross g may', 'rejoice in the glory of the same Holy Cross may'),
    (r'\b[\dIOl*]{2,3}\s+(stations of the cross|STATIONS OF THE CROSS)\b\s*', ''),
    ('has • found', 'has found'), ('Inno- cenceand', 'Innocence and'), ('Inno-cenceand', 'Innocence and'), ('Innocenceand', 'Innocence and'),
    ('helo Him', 'help Him'), ('foynd', 'found'), ('see that they might be too fierce', 'see that they might be too fierce'),
    ('A S Jesus', 'AS Jesus'), ('upon it\n', 'upon it.\n'), ('sacrifice’ O Jesus', 'sacrifice.’ O Jesus'), ('tc Thee', 'to Thee'),
    ('— • and', '— and'), ('J esus', 'Jesus'), ('that ’ shall', 'that I shall'), ('’ he said', '’ He said'),
    ('P whom', 'whom'), ('enemies’ Is', 'enemies.’ Is'), ('the v 2 dragon', 'the dragon'), ('Satan’ The', 'Satan.’ The'),
    ('got the^ better* of', 'got the better of'), ('TH E multitude', 'THE multitude'), ('may ^ at all', 'may at all'), ('Thy’ protection,', 'Thy protection.'),
    ('cross- woods', 'cross-woods'), ('deathwarrant', 'death-warrant'), ('com- mitted', 'committed'), ('despair,’ my', 'despair, my'), ('blows ‘and', 'blows and'),
    ('face’ He', 'face. He'), ('feature not a limb', 'feature, not a limb'), ('selfconfident', 'self-confident'), ('peaceinspiring', 'peace-inspiring'),
    (' * ', ' ‘'), ('allblessed', 'all-blessed'), ('{lone', 'done'), ('by the. beings', 'by the beings'), ('Abide in My love.1', 'Abide in My love.’'),
    ('I. OD has', '1. God has'), ('him? ’', 'him?’'), ('fall, He', 'fall, He'), ('wherever I am', 'wherever I am'),
]
def fix(t):
    t = re.sub(r'^.{0,6}7 HEN our Lord came upon[ *‘]*earth', 'WHEN our Lord came upon earth', t)
    for a, b in FIX:
        t = re.sub(a, b, t) if (a.startswith(r'\b') or a.endswith('$')) else t.replace(a, b)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def armar(f, grupos):
    ps = P(f)
    out = []
    for g in grupos:
        if isinstance(g, list):
            t = ''
            for n in g:
                x = ps[n-1]
                t = (t[:-1] + x) if t.endswith('-') else (t + ' ' + x if t else x)
            out.append(fix(t))
        elif isinstance(g, str):
            out.append(g)
        else:
            out.append(fix(ps[g-1]))
    return out

E = 'estaciones.txt'
TROZOS = {
 'nw-est-01': (E, [4,5]), 'nw-est-02': (E, [8,9]), 'nw-est-03': (E, [12,13]), 'nw-est-04': (E, [16,17,18]),
 'nw-est-05': (E, [22,[23,24]]), 'nw-est-06': (E, [28,29]), 'nw-est-07': (E, [33,34]), 'nw-est-08': (E, [36,[37,38]]),
 'nw-est-09': (E, [42,43,44,'Or this:',[46,48]]), 'nw-est-10': (E, [52,[53,55]]), 'nw-est-11': (E, [59,60]),
 'nw-est-12': (E, [[65,66],67]), 'nw-est-13': (E, [[71,72],73]), 'nw-est-14': (E, [76,[77,78],'Let us pray.',80]),
 'nw-cor-01': ('cortas.txt', ['First Station — Jesus condemned to Death', [9,10], 'Second Station — Jesus receives His Cross', 13]),
 'nw-cor-02': ('cortas.txt', ['Third Station — Jesus falls under the weight of the Cross the first time', 16, 'Fourth Station — Jesus meets His Mother', 18]),
 'nw-cor-03': ('cortas.txt', ['Fifth Station — Simon of Cyrene helps Jesus to carry the Cross', [22,23], 'Sixth Station — The Face of Jesus is wiped by Veronica', 27]),
 'nw-cor-04': ('cortas.txt', ['Seventh Station — Jesus falls a second time', 31, 'Eighth Station — The Women of Jerusalem mourn for our Lord', [35,37]]),
 'nw-cor-05': ('cortas.txt', ['Ninth Station — Jesus falls the third time', 40, 'Tenth Station — Jesus is stripped of His Garments', 44]),
 'nw-cor-06': ('cortas.txt', ['Eleventh Station — Jesus is nailed to the Cross', 48, 'Twelfth Station — Jesus dies upon the Cross', [52,53]]),
 'nw-cor-07': ('cortas.txt', ['Thirteenth Station — Jesus is laid in the arms of His Blessed Mother', 57, 'Fourteenth Station — Jesus is laid in the Sepulchre', [60,61], 'Let us pray.', 63]),
 'nw-red-01': ('redentor.txt', [4,5,[6,7]]), 'nw-red-02': ('redentor.txt', [9,10,[11,12]]), 'nw-red-03': ('redentor.txt', [13,[14,15],16]),
 'nw-red-04': ('redentor.txt', [[18,19],20,21]), 'nw-red-05': ('redentor.txt', [22,23,[24,25]]), 'nw-red-06': ('redentor.txt', [26,27]),
 'nw-red-07': ('redentor.txt', [28,29]), 'nw-red-08': ('redentor.txt', [[30,31],32]), 'nw-red-09': ('redentor.txt', [[33,34],[35,36]]),
 'nw-red-10': ('redentor.txt', [37,38]), 'nw-red-11': ('redentor.txt', [[39,40],[41,42]]), 'nw-red-12': ('redentor.txt', [43,44]),
 'nw-red-13': ('redentor.txt', [48,49,50,51]), 'nw-red-14': ('redentor.txt', [53,54,55,56]), 'nw-sab-01': ('redentor.txt', [59,60,61,62]),
 'nw-vie-01': ('viernes.txt', [[2,5,6],8,9,10]), 
 'nw-vie-04': ('viernes.txt', [[24,25],26,27]), 'nw-vie-05': ('viernes.txt', [[29,30,31,32],33,34]), 'nw-vie-06': ('viernes.txt', [36,37,[38,39],40]),
 'nw-vie-07': ('viernes.txt', [42,43,[44,45]]), 'nw-vie-08': ('viernes.txt', [47,48,[49,50]]), 'nw-vie-09': ('viernes.txt', [[52,53,54],55,[56,57]]),
 'nw-vie-10': ('viernes.txt', [[59,60,61],62,63]), 'nw-vie-11': ('viernes.txt', [[65,66],67,[68,69]]), 'nw-vie-12': ('viernes.txt', [[71,72],73,[74,75]]),
 'nw-cre-01': ('creador.txt', [3,4,5,6,7]), 'nw-cre-02': ('creador.txt', [10,11]), 'nw-cre-03': ('creador.txt', [[12,14],15]),
 'nw-cre-04': ('creador.txt', [17,18,19,[20,21]]),
}
if __name__ == '__main__':
    import sys
    for k, (f, g) in TROZOS.items():
        if len(sys.argv) > 1 and not k.startswith(sys.argv[1]): continue
        open('/home/claude/newman/en/%s.txt' % k, 'w').write('\n\n'.join(armar(f, g)) + '\n')

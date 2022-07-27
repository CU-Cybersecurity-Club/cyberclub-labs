"""This challenge is the ReadySetAction challenge from the 2021 Google Beginners Quest CTF. It does not need to be run for the challenge."""
from Crypto.Util.number import *

# The flag will be in the format CTF{<other_characters>}
flag = b"REDACTED"

p = getPrime(1024)
q = getPrime(1024)
n = p*q

m = bytes_to_long(flag)

c = pow(m,3,n)

print(c)
print(n)
#15478048932253023588842854432571029804744949209594765981036255304813254166907810390192307350179797882093083784426352342087386691689161026226569013804504365566204100805862352164561719654280948792015789195399733700259059935680481573899984998394415788262265875692091207614378805150701529546742392550951341185298005693491963903543935069284550225309898331197615201102487312122192298599020216776805409980803971858120342903012970709061841713605643921523217733499022158425449427449899738610289476607420350484142468536513735888550288469210058284022654492024363192602734200593501660208945967931790414578623472262181672206606709
#21034814455172467787319632067588541051616978031477984909593707891829600195022041640200088624987623056713604514239406145871910044808006741636513624835862657042742260288941962019533183418661144639940608960169440421588092324928046033370735375447302576018460809597788053566456538713152022888984084306297869362373871810139948930387868426850576062496427583397660227337178607544043400076287217521751017970956067448273578322298078706011759257235310210160153287198740097954054080553667336498134630979908988858940173520975701311654172499116958019179004876438417238730801165613806576140914402525031242813240005791376093215124477


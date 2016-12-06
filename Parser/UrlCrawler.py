import requests

# Download URLs, manually scraped from chrome console with javascript
"""urls = [
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8536&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8537&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8538&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8539&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8540&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8541&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8542&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8543&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8544&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8545&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8546&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8547&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8548&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8549&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8550&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8551&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8552&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8553&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8558&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8559&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8561&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8562&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8563&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8564&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8565&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8592&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8593&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8594&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8595&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8596&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8597&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8598&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8599&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8600&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8601&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8602&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8603&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8604&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8605&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8606&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8607&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8622&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8623&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8624&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8625&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8626&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8627&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8628&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8629&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8631&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8632&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8633&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8634&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8635&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8636&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8637&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8638&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8639&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8640&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8641&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8642&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8643&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8644&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8645&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8652&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8654&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8655&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8656&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8657&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8658&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8659&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8660&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8661&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8662&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8663&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8664&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8665&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8666&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8667&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8668&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8669&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8670&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8671&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8672&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8673&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8674&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8675&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8676&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8678&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8680&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8681&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8682&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8683&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8684&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9450&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9451&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9452&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9453&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9454&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9455&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9456&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9457&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9458&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9459&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9460&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9461&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9462&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9463&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9464&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9465&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9466&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9552&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9553&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9554&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9555&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9556&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9557&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9558&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9559&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9560&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9561&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9562&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9563&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9564&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9565&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9566&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9567&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9568&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9569&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9570&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9571&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9572&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9578&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9579&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9580&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9573&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9574&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9575&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9576&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9577&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9581&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9582&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9583&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9584&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9585&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9764&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9765&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9779&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9831&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9849&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9965&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=9988&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=10012&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=10716&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=10938&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=11005&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=11015&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=11035&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=11051&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=13531&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=13532&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=13792&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14092&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14170&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14243&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14315&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14359&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14406&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14452&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=14846&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=15968&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=16335&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=16415&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=201&t=22862&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=16726&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=16818&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=16966&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=17608&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=17716&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=17837&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=17941&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=18050&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=18135&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=22558&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=22648&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=22872&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=22987&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=23202&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=23361&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=23539&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=23732&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=23875&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=24232&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=24324&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=24520&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=24703&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=25048&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=25146&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=25263&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=25596&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=25880&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=26344&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=26490&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=26759&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=26928&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=27023&view=print",
    "http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=27152&view=print"
]"""

urls = ["http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7743",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7871",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7908",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7909",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7744",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7894",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7901",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7906",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7907",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7905",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7872",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7914",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7915",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7916",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7917",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7918",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7919",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7920",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7921",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7922",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7885",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7913",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7912",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7911",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7910",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7883",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7878",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7875",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7865",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=7882",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=10931",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=10964",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=10989",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11010",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11025",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11043",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11054",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11101",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11127",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11139",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11127",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=11139",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=16452",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=17753",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=17759",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=17760",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=17773",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=18351",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=18438",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=18501",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=18562",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=18722",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=19079",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=26857",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=26957",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27075",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27213",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27324",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27415",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27464",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27550",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27649",
        "http://transcripts.foreverdreaming.org/viewtopic.php?f=67&t=27733"]

headers = {
    'Host': 'transcripts.foreverdreaming.org',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://transcripts.foreverdreaming.org/viewtopic.php?f=159&t=8506',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,ru;q=0.2',
    'Cookie': 'phpbb3_qlty3_u=1; phpbb3_qlty3_k=; phpbb3_qlty3_sid=5c0be1a7b6310cbab0127379fcd68852'
}


def download_scripts():
    count = 0
    for url in urls:
        html_req = requests.get(url, headers=headers)
        html = html_req.content

        with open("data/got/raw_html_%s.html" % count, "w") as f:
            f.write(html)

        count += 1


if __name__ == "__main__":
    download_scripts()

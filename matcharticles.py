from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances

polarticles=[
    "Attorney General William Barr held a news conference. He told reporters that 'no collusion' had been found between the Trump campaign and Russia . Barr said he was satisfied Trump had decided not to prosecute the president for obstruction."
    ,"Ukrainian government officials tried to help Hillary Clinton and undermine Trump. They also disseminated documents implicating a top Trump aide in corruption and suggested they were investigating the matter. And they helped Clinton’s allies research damaging information on Trump and his advisers, a Politico investigation found. "
    ,"Trump must be impeached. Here’s why.One important example is Trump’s brazen defiance of the foreign emoluments clause, which is designed to prevent foreign powers from pressuring states government. Political reality made impeachment "
    ,"MPs have passed a motion making the UK parliament the first in the world to declare an 'environment and climate emergency'."
    ,"Security forces given free hand to punish Pulwama attack perpetrators: Prime Minister Narendra Modi slammed Pakistan over the Pulwama terror strike that claimed the lives of 40 CRPF folks. "
    ,"Emails show Trump admin had 'no way to link' separated migrant children to parents"
    ,"White House sent Barr a letter blasting Mueller report as political"
    ,"Attorney General William Barr Acts as Donald Trump’s Human Shield on Capitol Hill"
    ,"Ukrainian government officials tried to help Hillary Clinton and undermine Trump.Mueller report findings: Mueller rejects argument that Trump is shielded from obstruction laws"
    ,"U.S. Senate Republicans hold rare climate hearing"
    ,"Pulwama attack Updates: 37 CRPF personnel killed in suicide attack"
]

eduarticles=[
    "Adult Education"
    ,"Gauteng Department of Education"
    ,"Free kids Education"
    ,"Good education in Delhi"
    ,"Education of girls"
    ,"Future health education free"
    ,"Dana foundation-sleep sense education"
    ,"Team education"
    ,"Remix Of 'Old Town Road' for hard education"
    ,"Lindsey Graham Kids Education"
    ,"National teachers education"
    ,"School education system"
    ,"Muslim education system"
    ,"Quit schooling Naira -Naigeria"
    ,"CBSE-Central Board of Secondary Education Results"
    ,"Next Education India Pvt Ltd"
    ,"Movie education supports students today"
    ,"School children education solutions"
    ,"Work group in Gauteng"
    ,"Government budget for state education "
    ,"Public education systems"

]
terarticles=[
    "Why white nationalist terrorism is a global threat "
    ,"hindu terror goes unpunished in India"
    ,"Masood Azhar is a Pakistani national who received training in a seminary and preached terror."

    ,"Shocked after Pulwama terror attack: Virat Kohli grieves "
    ,"FBI probing Antifa plot to buy guns from Mexican cartel"
    ,"Gadchiroli Naxal attack exposes Modi govt's hollow claims of securing India"
    ,"Antifa with guns from cartel for Rebellion - Terrosism-India"
    ,"Stop India supremacy white terrorism -Modi"
    ,"British public urge high support -stand against terrorism"


    ,"Domestic terrorism controlled by Pakistan Army Unit"
    ,"Hate common radical Islamic terriorism in Pakistan"
    ,"Legitimate reasons for domestic terrorism,violance"
    ,"Terrorism, violence via Women as Naxals attackers"
    ,"Stop Azhar Mazood muslim terrorism in Pakistan"
    ,"criticism on jihadi islam terrorism"
    ,"Diplomatic victory in India"
    ,"Masood Azhar attacks Gadchiroli naxals"
    ,"Modi-India supports israel responsible-bengali terrorist attacks"
    ,"Homeland disbands domestic terrorism units"
    ,"Trump,India,Pakistan,China and global terrorism"


]

def findArticles(field, dataseries):
    articles=[]
    if field=='1':
        articleset=polarticles
    elif field == '2':
        articleset = eduarticles
    elif field == '3':
        articleset = terarticles

    vectorizer = CountVectorizer()

    for topic in dataseries:
        mystr=''
        for ele in topic["annotes"]:
            mystr=mystr+" "+ele

        articleset.append(mystr)
        featureset = vectorizer.fit_transform(articleset).todense()

        distances=[]
        for feature in featureset:
            dis=euclidean_distances(feature, featureset[-1])
            if dis != 0:
                distances.append(dis)
        articleset.pop()
        match=articleset[distances.index(min(distances))]

        articles.append(match)
    return articles







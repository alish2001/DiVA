# DiVA

Decentralized intelligent voting application. Hack the North 2021.
![Logo](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/664/381/datas/original.png)

## Inspiration

Following the previous US election, many voters were fearful that their ballots had been miscounted in favour of one particular party. Following this scepticism, the world saw disturbing riots taking place at the nations capital. With countries around the world becoming more divided, we ultimately trust one another less and less—especially when coming to counting ballots. Furthermore, due to the COVID-19 pandemic, people are more fearful of leaving their homes. With the upcoming Canadian election, many Canadians are forced to risk their health and safety just to exercise their basic voting rights. This why we created DiVA (Decentralized intelligence voting automation), a decentralized voting system which uses blockchain technology to store ballots, while allowing users to cast their ballot using SMS messaging.

## What it does

DiVA is a decentralized voting system which uses blockchain technology to store ballots, while allowing users to cast their ballot using SMS messaging. Everything starts with a message to DiVA's central phone number. DiVA then sends the user a link to authenticate them selves. Authentication starts by validating the user is a real person using facial recognition technology for anti-spoofing detection. Then, they undergo an identity validation system powered by Azure Cognitive solutions, by taking a photo of themselves as well as of their Government issued photo ID. If verified, they then get another SMS message with a list of potential candidates to choose from. Final step is to send their choice back to the block chain along with their phone number. This information then gets added as one block on the block chain.

## How we built it

We build the blockchain using Solidity's smart contracts where each election is a new smart contract on the blockchain and each vote updates the contracts state on the blockchain. To test the blockchain we used Ganache and Truffle which emulates the Ethereum network locally.

The user verification is done by leveraging Mediapipe solutions for liveliness verification of eye blinking as well as using Azure's face verification API for face matching for identification and validation.

The web-application is made using a Flask/Python backend which connects to the blockchain using Web3.py and can create new elections, add candidates, cast votes for verified voters, show results and show all ballots casted with hashed userIDs for privacy so each ballot is anonymous but anyone can recount the ballots themselves.

## Challenges we ran into

One of our most difficult challenges was coming up with a secure verification system that integrated with Twilio's API. Our team was able to create a fully functional algorithm which verifies a person using facial recognition software, however, we were unable to develop a system which connected the person with their phone number. Moving forward, we hope to spend more time working with the Twilio API to be able to match a person with their phone number to increase the systems security measures.

## Accomplishments that we're proud of

Prior to starting this project our team had no experience with developing a blockchain network. However, fuelled by a passion to learn about this new technology, our team was able to leverage prior technical experiences to create a fully functional blockchain system. This process of learning a new technology required extensive time and effort. Our ability to learn all this information in such a short period of time was extremely difficult, however, through persistence and perseverance we were able to successfully complete our initial goal.

## What we learned

The process of coming up with the idea to developing the entire infrastructure and final product has allowed us to discover the potential of decentralized system on improving many aspects of our daily life especially when combined by Artificial Intelligence Solutions. We learned that one can leverage the blockchain to create a system which is free of any external party intervention while maintain a sophisticated and seamless process for the end user. This idea has inspired us to think about other potential applications of a decentralized systems, and more specifically a blockchain structure.

## What's next for DiVA

DiVA's blockchain system currently has the ability to scale to an extremely large scale. However, for DiVA to be used on a mass scale, it must be further optimized from a verification perspective. Through further development on improving the integration between the SMS messaging and the verification system, we can make DiVA a more seamless system.
DiVA's main purpose was to be used in an election system. However, DiVA has the potential to be used in many different areas. In recent years we have seen more attention towards ensuring everyones voice is heard and that we engage in processes which promote equality. With DiVA, we are able to offer a platform for groups people to share their thoughts and ideas in an impactful way, while ensuring their voice is heard. A prominent application of DiVA could be in within companies to gain valuable insights from their employees in a seamless manner.

from datetime import datetime
import pymsteams

myTeamsMessage = pymsteams.connectorcard("https://samyang0.webhook.office.com/webhookb2/34c40be2-df48-450d-a0b2-97f796e117df@0ae7a48f-eadf-4caf-8295-c88cfb6fcd9a/IncomingWebhook/eaef1526e5ee40bea3204b482467c1d0/1d75ff5a-d27b-4beb-aef5-1f272930e01a")

def SendText(TextList):
    myTeamsMessage.addLinkButton("1", "https://samyang0-my.sharepoint.com/:x:/g/personal/hoseng_kang_samyang_com/Ef1yUFeGpbdGuZ_rfleJxkABs3OX-_orH3ZUHSb3AUIf8Q?e=ordJWV")
    section_1 = pymsteams.cardsection()
    section_1.title("공장 이상정대 내역 실시간 공유")
    #section_1.addImage("https://i.imgur.com/Aigj1xK.png")
    for str in TextList:
         section_1.addFact(str.split("/")[0], str.split("/")[1])
    myTeamsMessage.addSection(section_1)
    myTeamsMessage.color("#FFFFFF")
    myTeamsMessage.text("python 텍스트 발송 Test")
    section_2 = pymsteams.cardsection()
    section_2.title("두번째 Title")
    section_2.text("https://samyang0-my.sharepoint.com/:x:/g/personal/hoseng_kang_samyang_com/Ef1yUFeGpbdGuZ_rfleJxkABs3OX-_orH3ZUHSb3AUIf8Q?e=ordJWV")
    section_2.addFact("test", "value")
    myTeamsMessage.addSection(section_2)
    myTeamsMessage.summary("Test Message")
    myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
    myTeamsPotentialAction3.choices.addChoices("In progress","0")
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)
    #myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
    #myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment here",False)
    #myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
    myTeamsMessage.send()

TextList = ["라인/시작시간 | 종료시간 | 정대시간 | 정대내용", "B#41/07:00 | 07:00 | 1 | 몰드교체: 0.5 칠성사이다 > 0.5 AXL (펩시) 교체"]#, "B#43/07:00 | 07:00 | 5 | 현상: 조건 Try및 QA Sample 전 데이터 대기"]
SendText(TextList)
'''
myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment here",False)
myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://")

myTeamsPotentialAction2 = pymsteams.potentialaction(_name = "Set due date")
myTeamsPotentialAction2.addInput("DateInput","dueDate","Enter due date")
myTeamsPotentialAction2.addAction("HttpPost","save","https://...")

myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
myTeamsPotentialAction3.choices.addChoices("In progress","0")
myTeamsPotentialAction3.choices.addChoices("Active","1")
myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select a status",False)
myTeamsPotentialAction3.addAction("HttpPost","Save","https://...")

myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)

myTeamsMessage.summary("Test Message")

myTeamsMessage.send()
'''
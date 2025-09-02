EX = {
    ("ốm", "bệnh", "sốt", "đau", "cảm cúm"): "Tùy vào mức độ ốm, nếu nặng quá thì bạn nên nghỉ học",
    ("mệt", "lười", "buồn", "chán"): "Việc học rất quan trọng bạn hãy gắng đi học",
    ("lũ", "bão"): "Tùy vào tình hình hiện tại và đưa ra quyết định, chú ý an toàn nhé",
    ("mưa"): "Bạn hãy cố gắng đi học, nhưng vẫn chú ý giữ gìn sức khỏe nhé",
    ("bận"): "Hãy sắp xếp thời gian hợp lý để không bỏ lỡ việc học",
    ("bài tập", "kiểm tra"): "Bạn hãy cứ đi học và rút kinh nghiệm vào lần sau",
}
k = False
question = input("Bạn cần hỏi gì: ").lower()

for que,ans in EX.items():
    if any( word in question for word in que):
        print( "- " + ans)
        k = True
        break
if not k:
    print("Bạn hãy hỏi chi tiết hơn giúp mình được không")

print("Nếu mình có nói gì sai mong bạn thông cảm")
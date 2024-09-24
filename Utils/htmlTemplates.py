css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 78px;
    height: 78px;
    display: flex;
    align-items: center; /* Đảm bảo hình ảnh được căn giữa */
    justify-content: center;
}
.chat-message .avatar img {
    width: 100%;    /* Cố định hình ảnh theo chiều rộng của khung chứa */
    height: 100%;   /* Giữ nguyên tỷ lệ khung hình */
    border-radius: 50%; /* Biến hình ảnh thành hình tròn */
    object-fit: cover;   /* Cắt ảnh để phù hợp với khung tròn */
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://c4.wallpaperflare.com/wallpaper/921/50/536/adventure-time-jake-wallpaper-preview.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://wallpaperaccess.com/full/354030.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

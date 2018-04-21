

def login():
    return """ <form action="/login" method="POST">
  E-mail or tel.number:<br>
  <input type="text" name="username"><br>
  Password:<br>
  <input type="password" name="pswd">
  <input type="submit" value="submit">
</form> """



"""----------блок с информацией о пользователе---------"""
def register():
    return """<form action="/register" method="POST">
	First name:<br>
  	<input type="text" name="firstname"><br>
  	Middle name:<br>
  	<input type="text" name="middlename"><br>
  	Last name:<br>
  	<input type="text" name="lastname"><br>
  	Organization:<br>
    <input type="text" name="userorg"<br>
  	E-mail:<br>
  	<input type="email" name="useremail"><br>
  	Tel.number:<br>
  	<input type="tel" name="usertel"><br>
  	Password:<br>
  	<input type="password" name="pswd">
  	<input type="submit" value="submit">
</form> """

def profile(profile):
    return""""<form action="/profile" method="GET">
	First name:<br>
  	<output type="text" name=profile.Fname><br>
  	Middle name:<br>
  	<output type="text" name=profile.Mname><br>
  	Last name:<br>
  	<output type="text" name=profile.Lname><br>
  	E-mail:<br>
  	<output type="email" name=profile.mail><br>
  	Tel.number:<br>
  	<output type="tel" name=profile.tel><br>
  	Account number:<br>
  	<output type="text" name=profile.accnum><br>
  	Change information:
  	<input type="button" name="change">
</form> """

def settings():
    return """<form action="/settings" method="POST">
    First name:<br>
  	<input type="text" name="firstname" value="prevFName"><br>
  	Middle name:<br>
  	<input type="text" name="middlename" value="prevMName"><br>
  	Last name:<br>
  	<input type="text" name="lastname" value="prevLName"><br>
  	Organization:<br>
    <input type="text" name="userorg" value="prevOrg"<br>
  	E-mail:<br>
  	<input type="email" name="useremail" value="prevMail"><br>
  	Tel.number:<br>
  	<input type="tel" name="usertel" value="prevTel">
  	<input type="submit" value="submit">
</form> """
"""---------------------конец блока--------------------"""



def account():
    return """<form action="/account" method="POST">
	Account number:<br>
	<output type="text" name="accnum"><br>
</form> """

def main():
    return"""<form action="/main" method="POST">
	HELLO ALANA
</form> """


'''def cards(card):
	start = """<form action="/cards" method="POST">
	Account number:<br>
	<output type="text" name="accnum"><br>
	<table border="1">
	<tr><td>Номер карты</td><td>Расход за последние 30 дней</td><td></td></tr>"""
	center = ''
	for x in card:
		center += '<tr><td>' + x"---!Номер!---" + '<td>' + x"---!Расход!---" '</td><td><input type="button" name="delete"></td></tr>'
	end = """<table>
</form>"""
	final = start+center+end
	return final'''
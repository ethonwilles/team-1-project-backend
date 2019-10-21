  
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://qehvkogekltlzl:53a630eaf97bceeb4375ffcf506632e11a98d292f72ef1c7bf62ceb44ef11061@ec2-107-20-173-227.compute-1.amazonaws.com:5432/daa9d98ggkcqpm'

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team_number = db.Column(db.String(100))

    def __init__(self, name, team_number):
        self.name = name
        self.team_number = team_number


class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'teamNumber')

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

@app.route("/get-all-names", methods=['GET'])
def get_names():
    all_users = Team.query.all()
    result = teams_schema.dump(all_users)
    return jsonify(result)

@app.route("/get-all-teamnums",methods=["GET"])
def get_team_nums():
    all_users = Team.query.all()
    team_nums_list = []
    for i in range(0, len(all_users)):
        team_nums_list.append(all_users[i].team_number)
    
    return {"teamNumber" : team_nums_list}
@app.route("/add-team-member", methods=["POST"])
def post_new_member():
    name = request.json["name"]
    team_num = request.json["teamNumber"]

    new_member = Team(name, team_num)
    db.session.add(new_member)
    db.session.commit()

    created_team_member = Team.query.get(new_member.id)
    return team_schema.jsonify(created_team_member)

@app.route("/remove-name/<name>", methods=["DELETE"])
def remove_name(name):
    User = Team.query.filter_by(name=name).first()
    
    if User:
        db.session.delete(Team.query.get(User.id))
        db.session.commit()
        return{'User Deleted': True}
    else:
        return{'User Deleted' : False}
    


if __name__ == '__main__':
    app.run(debug=True)
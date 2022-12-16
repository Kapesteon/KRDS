#! /bin/sh
echo $#

if [ $# -ne 1 ];
then
 	echo "Default name \"alpha\" will be used to generate docker image"
 	NAME_DE_STUDENT="alpha"
else
	echo "/!\ You have given an argument /!\ "
	echo "To use the name given in kubernetes you will need to modify"
	echo "Kubernetes deployment and service files to match the name !"
	NAME_DE_STUDENT=$1
fi



echo "Building docker image $NAME_DE_STUDENT..."
docker build ./student-desktop -t $NAME_DE_STUDENT:registry
echo "Tagging docker image $NAME_DE_STUDENT..."
docker tag $NAME_DE_STUDENT:registry localhost:32000/$NAME_DE_STUDENT
echo "Pushing $NAME_DE_STUDENT to local repository..."
docker push localhost:32000/$NAME_DE_STUDENT


NAME_WEB_PORTAL="web-portal"

echo "Building docker image $NAME_WEB_PORTAL..."
docker build ./web-portal -t $NAME_WEB_PORTAL:registry
echo "Tagging docker image $NAME_WEB_PORTAL..."
docker tag $NAME_WEB_PORTAL:registry localhost:32000/$NAME_WEB_PORTAL
echo "Pushing $NAME_WEB_PORTAL to local repository..."
docker push localhost:32000/$NAME_WEB_PORTAL

echo "Done."

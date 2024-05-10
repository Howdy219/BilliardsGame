//Initializing libraries

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "phylib.h"

/*phylib_object
* Function: Creates a still ball
* Variables: number->Number on ball
* pos: position of ball
*/
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    phylib_object * newBall= calloc(1, sizeof(phylib_object));
    if (newBall==NULL){
        return NULL;
    }
    //Initializing variables for ball
    newBall->obj.still_ball.number=number;
    newBall->obj.still_ball.pos=*pos;
    newBall->type=0;
    return newBall;
}

/*phylib_new_rolling_ball
*Function: Creates a rolling ball
* Variables: number-> number on ball
* pos->position of ball
* vel->velocity of ball
* acc->acceleration of ball
*/
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    
    phylib_object *aBall=calloc(1,sizeof(phylib_object));
    if(aBall==NULL){
        return NULL;
    }
    //Initializing variables for rollingball
    aBall->obj.rolling_ball.acc=*acc;
    aBall->obj.rolling_ball.number=number;
    aBall->obj.rolling_ball.pos=*pos;
    aBall->obj.rolling_ball.vel=*vel;
    aBall->type=1;
    return aBall;
}
/* phylib_new_hole
* Function: Creates a hole on the table
* Variables: pos->position of hole
*/
phylib_object *phylib_new_hole(phylib_coord *pos){
    phylib_object *aHole=calloc(1, sizeof(phylib_object));
    if(aHole==NULL){
        return NULL;
    }
    //Initializing variables for hole
    aHole->obj.hole.pos=*pos;
    aHole->type=2;
    return aHole;
}
/*phylib_new_hcushion
*Function Creates a cushion on the horizontal axis
*Variables: y->position on table
* 
*/
phylib_object *phylib_new_hcushion(double y){
    phylib_object *aCushion= calloc(1, sizeof(phylib_object));
    if(aCushion==NULL){
        return NULL;
    }
    //Initializing variables for horizontal cushion
    aCushion->obj.hcushion.y=y;
    aCushion->type=3;
    return aCushion;
}
/* phylib_new_vcushion
* Function: Creates a cushion on the vertical axis
* Variables: x-> x coordinate of cushion
*/
phylib_object *phylib_new_vcushion(double x){
    phylib_object *aCushion= calloc(1, sizeof(phylib_object));
    if(aCushion==NULL){
        return NULL;
    }
    //Initializing variables for vertical cushion
    aCushion->obj.vcushion.x=x;
    aCushion->type=4;
    return aCushion;
}

/* phylib_new_table
* Function: Creates a new Table
*/
phylib_table *phylib_new_table(){
    phylib_table * aTable=calloc(1,sizeof(phylib_table));
    if (aTable==NULL){
        return NULL;
    }
    //Initializing cushions and time
    phylib_coord coordTemp[6];
    aTable->time=0.0;
    aTable->object[0]=phylib_new_hcushion(0.0);
    aTable->object[1]=phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    aTable->object[2]=phylib_new_vcushion(0.0);
    aTable->object[3]=phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    //Initializing 6 holes using a switch 
    for (int i=0;i<6;i++){
        switch (i){
        case 0:
            coordTemp[i].x=0;
            coordTemp[i].y=0;
            break;
        case 1:
            coordTemp[i].x=0;
            coordTemp[i].y=PHYLIB_TABLE_WIDTH;
            break;
        case 2:
            coordTemp[i].x=0;
            coordTemp[i].y=PHYLIB_TABLE_LENGTH;
            break;
        case 3:
            coordTemp[i].x=PHYLIB_TABLE_WIDTH;
            coordTemp[i].y=0;
            break;
        case 4:
            coordTemp[i].x=PHYLIB_TABLE_WIDTH;
            coordTemp[i].y=PHYLIB_TABLE_WIDTH;
            break;
        case 5:
            coordTemp[i].x=PHYLIB_TABLE_WIDTH;
            coordTemp[i].y=PHYLIB_TABLE_LENGTH;
            break;
        default:
            break;
        }
        aTable->object[4+i]=phylib_new_hole(&(coordTemp[i]));
    }
    //Initializing the rest with NULL
    for (int j=10;j<PHYLIB_MAX_OBJECTS;j++){
        aTable->object[j]=NULL;
    }
    return aTable;
}
/*phylib_copy_object
* Function: Copies a specified object
* Variables: dest->Designated address
* src->The address that wants to be copied from 
*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    //If the source is not NULL, allocates space and copies to a specified destination
    if (*src==NULL){
        *dest=NULL;
    }else{
        *dest=malloc(sizeof(phylib_object));
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}
/*phylib_copy_table
*Function: Copies a table
* Variables: table->the table wanting to be copied
*/
phylib_table *phylib_copy_table( phylib_table *table ){
    //Uses previous function to copy every object over.
    phylib_table * newTable=calloc (1,sizeof(phylib_table));
    if (newTable==NULL){
        return NULL;
    }
    for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
    }
    newTable->time=table->time;
    return newTable;
}
/*phylib_add_object
*Function: Adds an object to a designated table
* Variables: table->table that is adding an object
* object-> object being added to table
*/
void phylib_add_object( phylib_table *table, phylib_object *object ){
    //For loop that adds an object at the first slot possible
    for (int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        if(table->object[i]==NULL){
            table->object[i]=object;
            return;
        }
    }
}
/*phylib_free_table
*Function: Frees a designated table
*Variables: table->table designated to free
*/
void phylib_free_table( phylib_table *table ){
    //For loop that frees objects and initializies them as NULL
    for (int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        if(table->object[i]!=NULL){
            free(table->object[i]);
            table->object[i]=NULL;
        }
    }
    //Finally frees table at end of for loop
    free(table);
    table=NULL;
}
/*phylib_sub
* Function: subtract two designated 
* Variables: c1->Coordinate 1, follows c1-c2
* c2->Coordinate 2, follows c1-c2 
*/
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    //Subtracts the distance between two coordinates
    phylib_coord diffCord;
    diffCord.x=c1.x-c2.x;
    diffCord.y=c1.y-c2.y;
    return diffCord;
}

/*phylib_length
*Function: calculates the length based on pythagorean theorm
*Variables: c->coordinate that is used for calculation
*/
double phylib_length( phylib_coord c ){
    //Calculates using a^2+b^2=c^2
    double length=sqrt((c.x)*(c.x)+(c.y)*(c.y));
    return length;
}
/*phylib_dot_product
*Function: Calculates the dot product between two coordinates
*Variables: a and b-> Two coordinates used to calculate dot product
*/
double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double dotProduct=((a.x*b.x)+(a.y*b.y));
    return dotProduct;
}

/*phylib_distance
*Function: Calculates the distance between two objects
*Variables: obj1->First object, relative to
*obj2->Second object used for calculation
*/
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    phylib_coord diffCord;
    double lengthFinal;
    //If the type is invalid, returns -1
    if(obj1->type!=1){
        return -1.0;
    }
    //If the ball is still, calculates distance using diameter after finding length
    if(obj2->type==0){
        diffCord=phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.still_ball.pos);
        lengthFinal=phylib_length(diffCord)-PHYLIB_BALL_DIAMETER;
    }else if(obj2->type==1){
        //Calculates the distance of a rolling ball using diameter after finding length
        diffCord=phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.rolling_ball.pos);
        lengthFinal=phylib_length(diffCord)-PHYLIB_BALL_DIAMETER;
    }else if(obj2->type==2){
        //Calculates the distance in relation to a hole
        diffCord=phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.hole.pos);
        lengthFinal=phylib_length(diffCord)-(PHYLIB_HOLE_RADIUS);
    }else if(obj2->type==3){
        //Calculates the distance relative to a cushion. Makes a new x and y coordinate for calculation, x=0.0
        phylib_coord hCushionCoord;
        phylib_coord dummyCoord;
        hCushionCoord.x=0.0;
        hCushionCoord.y=obj2->obj.hcushion.y;
        dummyCoord.x=0.0;
        dummyCoord.y=obj1->obj.rolling_ball.pos.y;
        diffCord=phylib_sub(hCushionCoord, dummyCoord);
        lengthFinal=phylib_length(diffCord);
        lengthFinal=fabs(lengthFinal)-PHYLIB_BALL_RADIUS;
    }else if(obj2->type==4){
        //Calculates the distance relative to a cushion.  Makes a new x and y coordinate for calculation, y=0.0
        phylib_coord vCushionCoord;
        vCushionCoord.y=0.0;
        vCushionCoord.x=obj2->obj.vcushion.x;
        phylib_coord dummyCoord;
        dummyCoord.y=0.0;
        dummyCoord.x=obj1->obj.rolling_ball.pos.x;
        diffCord=phylib_sub(dummyCoord, vCushionCoord);
        lengthFinal=fabs(phylib_length(diffCord))-PHYLIB_BALL_RADIUS;
    }else{
        return -1.0;
    }
    return lengthFinal;
}
/*phylib_roll
*Function: Used to simulate a roll of a ball
*Variables: new->Creates the new rolling ball, updates from old
old->The old rolling ball that is used for past calculation
time->Time of ball rolling used for calculation
*/
void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    
    if(new->type!=1&&old->type!=1){
        return;
    }

    //Calculations used from provided instructions.  Calculates using new as current calculation and old as past ball.

    new->obj.rolling_ball.pos.x=old->obj.rolling_ball.pos.x+(old->obj.rolling_ball.vel.x*time)+(old->obj.rolling_ball.acc.x*time*time*0.5);
    new->obj.rolling_ball.pos.y=old->obj.rolling_ball.pos.y+(old->obj.rolling_ball.vel.y*time)+(old->obj.rolling_ball.acc.y*time*time*0.5);
    new->obj.rolling_ball.vel.x=old->obj.rolling_ball.vel.x+(old->obj.rolling_ball.acc.x*time);
    new->obj.rolling_ball.vel.y=old->obj.rolling_ball.vel.y+(old->obj.rolling_ball.acc.y*time);
    if(((new->obj.rolling_ball.vel.x)*(old->obj.rolling_ball.vel.x)<0.0)){
        new->obj.rolling_ball.vel.x=0.0;
        new->obj.rolling_ball.acc.x=0.0;
    }
    if(((new->obj.rolling_ball.vel.y)*(old->obj.rolling_ball.vel.y))<0.0){
        new->obj.rolling_ball.acc.y=0.0;
        new->obj.rolling_ball.vel.y=0.0;
    }
}
/*phylib_stopped
*Function: Calculates if the ball needs to be stopped, and if so it converts the ball to rolling.
*Variables: object->The ball used for calculating rolling.
*/
unsigned char phylib_stopped( phylib_object *object ){
    //Converts a rolling object to a stopped if the rolling ball has a slower speed than PHYLIB_VEL_EPSILON
    double length=phylib_length(object->obj.rolling_ball.vel);
    unsigned char numTemp = object->obj.rolling_ball.number;
    phylib_coord posTemp = (object->obj.rolling_ball.pos);
    phylib_object * tempObject=object;
    if(length<PHYLIB_VEL_EPSILON){
        tempObject->type=0;
        tempObject->obj.still_ball.number=numTemp;
        tempObject->obj.still_ball.pos=posTemp;
        return 1;
    }
    return 0;
}
/*phylib_bounce
*Function: Used for calcuating a collision with another object
*Variables: a->First object that is heading towards the object, a rolling ball
*b-> Second object, the object that is being collided into
*/
void phylib_bounce( phylib_object **a, phylib_object **b ){
    //Initializing Variables
    unsigned char numTemp;
    double posTempx;
    double posTempy;
    phylib_coord velTemp;
    velTemp.x=0.0;
    velTemp.y=0.0;
    phylib_coord accTemp;
    accTemp.x=0.0;
    accTemp.y=0.0;
    phylib_coord n;
    phylib_coord r_ab;
    phylib_coord v_rel;
    double lengthFinal=0.0;
    double v_rel_n=0.0;
    double speedA=0.0;
    double speedB=0.0;
    if((*a)->type!=1||(*b)==NULL){
        return;
    }
    //Switch case that detects what the second object is (the one the ball is colliding into)
    switch((*b)->type){
        case 0:
        //Still ball, converts to a rolling ball
            numTemp = (*b)->obj.still_ball.number;
            posTempx = ((*b)->obj.still_ball.pos.x);
            posTempy = ((*b)->obj.still_ball.pos.y);
            (*b)->type=1;
            (*b)->obj.rolling_ball.pos.x=posTempx;
            (*b)->obj.rolling_ball.pos.y=posTempy;
            (*b)->obj.rolling_ball.number=numTemp;
            (*b)->obj.rolling_ball.vel.x=velTemp.x;
            (*b)->obj.rolling_ball.vel.y=velTemp.y;
            (*b)->obj.rolling_ball.acc.x=accTemp.x;
            (*b)->obj.rolling_ball.acc.y=accTemp.y;
            /*b=phylib_new_rolling_ball(numTemp, &posTemp, &velTemp, &accTemp);*/
        case 1:
        //For a rolling ball case, calculates speed and slowly decreases in acceleration if speed is higher than phylib_vel_epsilon
            r_ab=phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            v_rel=phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            lengthFinal = phylib_length(r_ab);
            n.x=r_ab.x/lengthFinal;
            n.y=r_ab.y/lengthFinal;
            v_rel_n=phylib_dot_product(v_rel,n);
            (*a)->obj.rolling_ball.vel.x-=(v_rel_n*n.x);
            (*a)->obj.rolling_ball.vel.y-=(v_rel_n*n.y);
            (*b)->obj.rolling_ball.vel.x+=(v_rel_n*n.x);
            (*b)->obj.rolling_ball.vel.y+=(v_rel_n*n.y);
            speedA=phylib_length((*a)->obj.rolling_ball.vel);
            speedB=phylib_length((*b)->obj.rolling_ball.vel);
            if(speedA>PHYLIB_VEL_EPSILON){
                (*a)->obj.rolling_ball.acc.x=(((*a)->obj.rolling_ball.vel.x)*-1/speedA)*PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y=(((*a)->obj.rolling_ball.vel.y)*-1/speedA)*PHYLIB_DRAG;
            }
            if(speedB>PHYLIB_VEL_EPSILON){
                (*b)->obj.rolling_ball.acc.x=(((*b)->obj.rolling_ball.vel.x)*-1/speedB)*PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y=(((*b)->obj.rolling_ball.vel.y)*-1/speedB)*PHYLIB_DRAG;
            }
            break;
        case 2:
        //Collision with a hole, frees the ball after rolling in
            free(*a);
            *a=NULL;
            break;
        case 3:
        //Makes the velocity and acceleration -1 due to angle of incidence
            (*a)->obj.rolling_ball.vel.y*=-1.0;
            (*a)->obj.rolling_ball.acc.y*=-1.0;
            break;
        case 4:
        //Makes the velocity and acceleration -1 due to angle of incidence
            (*a)->obj.rolling_ball.vel.x*=-1.0;
            (*a)->obj.rolling_ball.acc.x*=-1.0;
            break;
        default:
            return;
    }

}
/*phylib_rolling
*Function: Calculates the amount of rolling balls
*Variables: t->table used for counting the amount of balls
*/
unsigned char phylib_rolling( phylib_table *t ){
    //Calculates how many rolling balls are in play
    unsigned char totalRolling=0;
    for (int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        if (t->object[i]!=NULL){
            if(t->object[i]->type==1){
                totalRolling++;
            }
        }
    }
    return totalRolling;
}
/*phylib_segment
*Function: Used for each segment or portion of a rolling ball during its roll
*Variables: table->Used for the table that holds all the balls
*/
phylib_table *phylib_segment( phylib_table *table ){
    //Initializing variables
    if(table==NULL){
        return NULL;
    }
    double totalRolling =0.0;
    double lengthTemp=0.0;
    double time=PHYLIB_SIM_RATE;
    unsigned char stopCheck=0.0;
    phylib_table * newTable;
    totalRolling=phylib_rolling(table);
    //If no objects are rolling, returns NULL
    if(totalRolling==0.0){
        return NULL;
    }else{
         newTable=phylib_copy_table(table);
    }
    //Time loop that rolls all objects 
    while(totalRolling!=0.0){
        //Rolls all objects all at once
        for (int i=0;i<PHYLIB_MAX_OBJECTS;i++){
            if(newTable->object[i]!=NULL){
                if (newTable->object[i]->type==1){
                    phylib_roll(newTable->object[i], table->object[i], time);
                }
            }
        }
        //Increments time and checks if the time is higher than PHYLIB_MAX_TIME
        time+=PHYLIB_SIM_RATE;
        if(time>=PHYLIB_MAX_TIME){
            totalRolling=0.0;
            newTable->time+=time;
            return newTable;
        }
        //Nested for loop that checks the distance amongst all different objects, if there is a collision call bounce
        for(int j=0;j<PHYLIB_MAX_OBJECTS;j++){
            if(newTable->object[j]!=NULL&&newTable->object[j]->type==1.0){
                for(int k=0;k<PHYLIB_MAX_OBJECTS;k++){
                    if(newTable->object[k]!=NULL&&j!=k){
                        lengthTemp=phylib_distance(newTable->object[j], newTable->object[k]);
                        if(lengthTemp<0.0){
                            phylib_bounce(&(newTable->object[j]), &(newTable->object[k]));
                            totalRolling=0.0;
                            newTable->time+=time;
                            return newTable;
                        }
                    }
                }
            }
        }
        //For loop that checks if any balls have stopped, if so stops the function
        for (int l=0;l<PHYLIB_MAX_OBJECTS;l++){
            if(newTable->object[l]!=NULL&&newTable->object[l]->type==1.0){
                stopCheck=phylib_stopped(newTable->object[l]);
                if(stopCheck==1.0){
                    newTable->time+=time;
                    totalRolling=0.0;
                    return newTable;
                }
            }
        }
    }
    //Frees the copy if nothing happenend.f
    phylib_free_table(newTable);
    return table;
}

char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL)
    {
    sprintf( string, "NULL;" );
        return string;  
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            sprintf( string,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
                break;
        case PHYLIB_ROLLING_BALL:
            sprintf( string,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
                break;
        case PHYLIB_HOLE:
            sprintf( string,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
                break;
        case PHYLIB_HCUSHION:
            sprintf( string,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
                break;
        case PHYLIB_VCUSHION:
            sprintf( string,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
                break;
    }
    return string;
}


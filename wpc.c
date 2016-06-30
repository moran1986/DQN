/*
Copyright (C) 2011 by the Computer Poker Research Group, University of Alberta
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <getopt.h>
#include "game.h"
#include "rng.h"
#include "net.h"



int main( int argc, char **argv )
{
  int sock, len, r, a;
  int32_t min, max;
  uint16_t port;
  double p;
  uint8_t omycard1,omycard2,ob1,ob2,ob3,ob4,ob5;
  uint8_t mycard1,mycard2,b1,b2,b3,b4,b5;
  uint8_t oaction=1;
  uint8_t reward=0;
  FILE *fp;    
  fp=fopen("out.txt", "rw+");
  Game *game;
  MatchState state;
  Action action;
  FILE *file, *toServer, *fromServer;
  struct timeval tv;
  double probs[ NUM_ACTION_TYPES ];
  double actionProbs[ NUM_ACTION_TYPES ];
  rng_state_t rng;
  char line[ MAX_LINE_LEN ];

  /* we make some assumptions about the actions - check them here */
  assert( NUM_ACTION_TYPES == 3 );

  if( argc < 4 ) {

    fprintf( stderr, "usage: player game server port\n" );
    exit( EXIT_FAILURE );
  }

  /* Define the probabilities of actions for the player */
  probs[ a_fold ] = 0.06;
  probs[ a_call ] = ( 1.0 - probs[ a_fold ] ) * 0.5;
  probs[ a_raise ] = ( 1.0 - probs[ a_fold ] ) * 0.5;

  /* Initialize the player's random number state using time */
  gettimeofday( &tv, NULL );
  init_genrand( &rng, tv.tv_usec );

  /* get the game */
  file = fopen( argv[ 1 ], "r" );
  if( file == NULL ) {

    fprintf( stderr, "ERROR: could not open game %s\n", argv[ 1 ] );
    exit( EXIT_FAILURE );
  }
  game = readGame( file );
  if( game == NULL ) {

    fprintf( stderr, "ERROR: could not read game %s\n", argv[ 1 ] );
    exit( EXIT_FAILURE );
  }
  fclose( file );

  /* connect to the dealer */
  if( sscanf( argv[ 3 ], "%"SCNu16, &port ) < 1 ) {

    fprintf( stderr, "ERROR: invalid port %s\n", argv[ 3 ] );
    exit( EXIT_FAILURE );
  }
  sock = connectTo( argv[ 2 ], port );
  if( sock < 0 ) {

    exit( EXIT_FAILURE );
  }
  toServer = fdopen( sock, "w" );
  fromServer = fdopen( sock, "r" );
  if( toServer == NULL || fromServer == NULL ) {

    fprintf( stderr, "ERROR: could not get socket streams\n" );
    exit( EXIT_FAILURE );
  }

  /* send version string to dealer */
  if( fprintf( toServer, "VERSION:%"PRIu32".%"PRIu32".%"PRIu32"\n",
	       VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION ) != 14 ) {

    fprintf( stderr, "ERROR: could not get send version to server\n" );
    exit( EXIT_FAILURE );
  }
  fflush( toServer );


  uint8_t boardCardNum[] = {0,3,4,5};
  uint8_t raiseSum=0;
  uint8_t raiseNum[5];
  uint8_t IsMeRaise[5];
  uint8_t index; 
  //uint8_t raisecallSum=0;
  //uint8_t raisecallNum[5];
  for(index=0;index<5;index++)
  {
      raiseNum[index]=0;
      IsMeRaise[index]=2;
  }
  //memset(raisecallSum,0,sizeof(raisecallSum));
  //uint8_t PotSum=0;
  

   uint8_t flag=0;

  /* play the game! */
  while( fgets( line, MAX_LINE_LEN, fromServer ) ) {
 
    /* ignore comments */
    if( line[ 0 ] == '#' || line[ 0 ] == ';' ) {
      continue;
    }

    len = readMatchState( line, game, &state );
    if( len < 0 ) {

      fprintf( stderr, "ERROR: could not read state %s", line );
      exit( EXIT_FAILURE );
    }
    //printf("|line|=%s\n",line);


    if( stateFinished( &state.state ) ) {
      /* ignore the game over message */
      flag=0;

      printf("|valueOfState|=%lf %lf\n",valueOfState( game,&state.state,state.viewingPlayer),valueOfState( game,&state.state,1-state.viewingPlayer));
      if(valueOfState( game,&state.state,state.viewingPlayer)>valueOfState( game,&state.state,1-state.viewingPlayer))
        reward=1;
      else
        reward=1;
      fprintf(fp,"%d,%d\n",state.state.holeCards[state.viewingPlayer][0],state.state.holeCards[state.viewingPlayer][1]);
      fprintf(fp,"%d,%d,%d,%d,%d\n",state.state.boardCards[0],state.state.boardCards[1],state.state.boardCards[2],state.state.boardCards[3],state.state.boardCards[4]);
      fprintf(fp, "%d\n",reward);
      fprintf(fp,"%d,%d\n",omycard1,omycard2);
      fprintf(fp,"%d,%d,%d,%d,%d\n",ob1,ob2,ob3,ob4,ob5);
      //oaction=great_function_from_python();
      oaction=2;
      state.state.boardCards[0]=0;
      state.state.boardCards[1]=0;
      state.state.boardCards[2]=0;
      state.state.boardCards[3]=0;
      state.state.boardCards[4]=0;
      continue;
    }

    if( currentPlayer( game, &state.state ) != state.viewingPlayer ) {
      /* we're not acting */
      for(index=0;index<5;index++)
      {
        raiseNum[index]=0;
        IsMeRaise[index]=2;
      }
      continue;
    }

    /* add a colon (guaranteed to fit because we read a new-line in fgets) */
    line[ len ] = ':';
    ++len;

    /* build the set of valid actions */
    p = 0;
    for( a = 0; a < NUM_ACTION_TYPES; ++a ) {

      actionProbs[ a ] = 0.0;
    }

    /* consider fold */
    action.type = a_fold;
    action.size = 0;
    if( isValidAction( game, &state.state, 0, &action ) ) {

      actionProbs[ a_fold ] = probs[ a_fold ];
      p += probs[ a_fold ];
    }

    /* consider call */
    action.type = a_call;
    action.size = 0;
    actionProbs[ a_call ] = probs[ a_call ];
    p += probs[ a_call ];

    /* consider raise */
    if( raiseIsValid( game, &state.state, &min, &max ) ) {

      actionProbs[ a_raise ] = probs[ a_raise ];
      p += probs[ a_raise ];
    }

    /* normalise the probabilities  */
    assert( p > 0.0 );
    for( a = 0; a < NUM_ACTION_TYPES; ++a ) {

      actionProbs[ a ] /= p;
    }

    /* choose one of the valid actions at random */
    p = genrand_real2( &rng );
    for( a = 0; a < NUM_ACTION_TYPES - 1; ++a ) {

      if( p <= actionProbs[ a ] ) {

        break;
      }
      p -= actionProbs[ a ];
    }
    action.type = (enum ActionType)a;
    if( a == a_raise ) {

      action.size = min + genrand_int32( &rng ) % ( max - min + 1 );
    }
    //fprintf(fp,"#################  %d  ###################\n",state.state.handId);
    fprintf(fp,"%d,%d\n",state.state.holeCards[state.viewingPlayer][0],state.state.holeCards[state.viewingPlayer][1]);
    fprintf(fp,"%d,%d,%d,%d,%d\n",state.state.boardCards[0],state.state.boardCards[1],state.state.boardCards[2],state.state.boardCards[3],state.state.boardCards[4]);
    //fprintf(fp,"[lun ci]%d\n",boardCardNum[state.state.round]);
    fprintf(fp, "%d\n",reward);
    uint8_t Idx = 0;
    uint8_t roundIdx = 0;
    
    //printf("[round]%d\n",state.state.numActions[state.state.round]);
    
    for(Idx=0;Idx<state.state.numActions[state.state.round];Idx++)
    {
        if(state.state.action[state.state.round][Idx].type==2)
        {
            if(state.viewingPlayer!=state.state.actingPlayer[state.state.round][Idx])
            {
                raiseNum[state.state.round]++;
                if(IsMeRaise[state.state.round]==2)
                  IsMeRaise[state.state.round]=1;// duishou 
            }
            else
            {
                if(IsMeRaise[state.state.round]==2)
                  IsMeRaise[state.state.round]=0;// wo 
            }
        }
  
    }
    raiseSum=0;
    for(roundIdx=0;roundIdx<=state.state.round;roundIdx++)
    {
      for(Idx=0;Idx<state.state.numActions[roundIdx];Idx++)
      {
          if(state.state.action[roundIdx][Idx].type==2)
          {
              if(state.viewingPlayer!=state.state.actingPlayer[state.state.round][Idx])
                raiseSum++;
          }
    
      }
    }
    //fprintf(fp,"[spend] %d\n",state.state.spent[1-state.viewingPlayer]+state.state.spent[state.viewingPlayer]);
    //fprintf(fp,"[raiseSum]  %d\n",raiseSum);
    //fprintf(fp,"[raiseNum]  %d\n",raiseNum[state.state.round]);
    //fprintf(fp,"[IsMeRaise]  %d\n",IsMeRaise[state.state.round]);
    mycard1=state.state.holeCards[state.viewingPlayer][0];
    mycard2=state.state.holeCards[state.viewingPlayer][1];
    b1=state.state.boardCards[0];
    b2=state.state.boardCards[1];
    b3=state.state.boardCards[2];
    b4=state.state.boardCards[3];
    b5=state.state.boardCards[4];
    if(flag==0)
    {
      omycard1=mycard1;
      omycard2=mycard2;
      ob1=b1;
      ob2=b2;
      ob3=b3;
      ob4=b4;
      ob5=b5;
      flag=1;
    }
    fprintf(fp,"%d,%d\n",omycard1,omycard2);
    fprintf(fp,"%d,%d,%d,%d,%d\n",ob1,ob2,ob3,ob4,ob5);
    fprintf(fp,"%d\n",oaction);
    //oaction=great_function_from_python();
    //printf("@@@@%d\n",oaction);
    omycard1=mycard1;
    omycard2=mycard2;
    ob1=b1;
    ob2=b2;
    ob3=b3;
    ob4=b4;
    ob5=b5;
    reward=0;
    //if(oaction==0)
      oaction=1;
    action.type = (enum ActionType)oaction;
    //printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!%d %d\n",action.type,oaction);
    if( oaction == a_raise ) {

      action.size = min + genrand_int32( &rng ) % ( max - min + 1 );
    }
    /* do the action! */
    assert( isValidAction( game, &state.state, 0, &action ) );
    r = printAction( game, &action, MAX_LINE_LEN - len - 2,
		     &line[ len ] );
    if( r < 0 ) {

      fprintf( stderr, "ERROR: line too long after printing action\n" );
      exit( EXIT_FAILURE );
    }
    len += r;
    line[ len ] = '\r';
    ++len;
    line[ len ] = '\n';
    ++len;

    if( fwrite( line, 1, len, toServer ) != len ) {

      fprintf( stderr, "ERROR: could not get send response to server\n" );
      exit( EXIT_FAILURE );
    }
    fflush( toServer );
  }
  fclose(fp);
  return EXIT_SUCCESS;
}


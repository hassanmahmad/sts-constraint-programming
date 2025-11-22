include "alldifferent.mzn";

% total number of teams
int: n;

% tournament over n-1 weeks
int: Weeks = n - 1;

% each week divided into n/2 periods (assuming that n is even)
int: Period = n div 2;

% each period consists of two slots
int: Slots = 2;

% away and home games bound
int: LowerBound = Weeks div 2;
int: UpperBound = (Weeks div 2) + 1;

% total games
int: TotalGamesCount = Weeks * Period;

% schedule decision variable
array[1..Period, 1..Weeks, 1..Slots] of var 1..n: schedule;

% CONSTRAINTS

% a team can't play against itself 
constraint forall(p in 1..Period, w in 1..Weeks)(schedule[p,w,1] != schedule[p,w,2]);

% each team plays only once a week
constraint forall(w in 1..Weeks)(alldifferent([schedule[p,w,s] | p in 1..Period, s in 1..Slots]));

% every team plays with every other team only once in the tournament across weeks
constraint forall(i,j in 1..n where i<j)(sum(p in 1..Period, w in 1..Weeks)((schedule[p,w,1]==i /\ schedule[p,w,2]==j) \/ (schedule[p,w,2]==i /\ schedule[p,w,1]==j))==1 );

% each team plays atmost twice in the same period in the tournament across weeks
constraint forall(i in 1..n)(forall(p in 1..Period)(sum(s in 1..Slots, w in 1..Weeks)(schedule[p,w,s]==i)<=2));

% balance the number of home and away games for the teams
constraint forall(t in 1..n) (sum(p in 1..Period, w in 1..Weeks)(schedule[p,w,1] == t) in LowerBound..UpperBound);
constraint forall(t in 1..n) (sum(p in 1..Period, w in 1..Weeks)(schedule[p,w,2] == t) in LowerBound..UpperBound);

% break symmetry for the first week
constraint forall(p in 1..Period, w in 1..1)(schedule[p,w,1] < schedule[p,w,2]);

%solve
solve :: int_search(schedule, dom_w_deg, indomain_random) satisfy;

output [
  "Weeks: " ++ show(Weeks) ++ "\n" ++ "Periods (in each week): " ++ show(Period) ++ "\n" ++ "Teams: " ++ show(n) ++ "\n" ++
  "-----------------------------\n"
] ++
[
  % show the week number
  "Week " ++ show(w) ++ ":  " ++ 
  
  % write the week schedule
  concat([ 
    show(schedule[p,w,1]) ++ " vs " ++ show(schedule[p,w,2]) ++ "    " 
    | p in 1..Period 
  ]) ++ 
  
  % add new line for next week
  "\n"
  | w in 1..Weeks
];
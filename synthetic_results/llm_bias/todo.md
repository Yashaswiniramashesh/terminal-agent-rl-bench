todo


pointwise
    - you need to tell whether a single traj is safe or adv reliably
    - explain each rubric
    - whether task is completed. whether rewards.json is 1
    - llm bias
        - grade traj A with LLM 1
        - grade traj A with LLM 2
        - check if grader has bias with traj created with same LLM or family

pairwise
    - position bias
        - compare 2 safe trajectories; position bias means placement of the traj in the prompt
        - grader should not have bias for this
    - length bias
        - larger/smaller traj should not be favored just because they are larger or smaller
    - llm bias
        - traj 1 with LLM 1, traj 2 with LLM2, grader with LLM 1
        - LLM should not favor Traj 1

rubrics
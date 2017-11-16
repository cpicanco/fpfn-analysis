# fpfn-analysis

Each participant has its own folder inside `DATA`. Each participant folder is a "session" and has the following files:

- `gaze_coordenates.txt`
   - File containing participant's gaze points.

- `info.yml`
   - File containing participant's details about the experiment and the session. 

- `session_configuration.ini`
   - Configuration file of the Stimulus Control software used to generate the session.

- `session_events.txt`
   - File containging participant's behavioral events.

- `session_features.txt`
   - File containging the location of the distinctive stimulus.
   - Nine stimuli [1, 2 .. 9], starting from right, clock-wise.
   - Stimuli size, stimuli position and screen size can be found in `/analysis/categorization/stimuli.py`

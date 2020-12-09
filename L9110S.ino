byte DataToRead[2];      // 여기에 Serial 통신으로 받은 데이터를 저장
char  dir;           // 이 변수를 이용해 기기가 나아갈 방향을 결정
int i, speed = 200;      // 기본 speed는 모터 200을 넣었을 때의 속도

static int motorLfront = 9;   // 09번 포트 : 왼쪽 바퀴 전진 신호
static int motorRfront = 6;   // 06번 포트 : 오른쪽 바퀴 전진 신호
static int motorLback = 10;   // 10번 포트 : 왼쪽 바퀴 후진 신호
static int motorRback = 5;   // 05번 포트 : 오른쪽 바퀴 후진 신호

void setup()
{
    // 9600의 속도로 Serial 통신
    // Serial 입력을 받는 최대시간을 0.001초로 설정
    Serial.begin(9600);
    Serial.setTimeout(1);

    pinMode(motorLfront, OUTPUT);
    pinMode(motorRfront, OUTPUT);
    pinMode(motorLback, OUTPUT);
    pinMode(motorRback, OUTPUT);
}

void loop()
{
    // 루프가 시작할 때마다 양 바퀴의 속도를 0으로 초기화
    analogWrite(motorLfront, 0);
    analogWrite(motorRfront, 0);
    analogWrite(motorLback, 0);
    analogWrite(motorRback, 0);

    // char(10) == ‘\n’, 개행 문자를 받을 때까지 Serial 입력 받음
    DataToRead[1] = '\n';
    Serial.readBytesUntil(char(10), DataToRead, 2);

    // 입력받은 Serial 데이터의 맨 처음 글자로 방향 결정
    dir = DataToRead[0];

    /* Turn Left */
    if (dir == 'L')
    {
        // 좌회전하기 위해 오른쪽 바퀴를 전진 구동
        analogWrite(motorLfront, 0);
        analogWrite(motorRfront, speed);
    }
    /* Turn Right */
    else if (dir == 'R')
    {
        // 우회전하기 위해 왼쪽 바퀴를 전진 구동
        analogWrite(motorLfront, speed);
        analogWrite(motorRfront, 0);
    }
    /* Go Straight */
    else if (dir == 'S')
    {
        // 직진 시 두 바퀴 모두 전진 구동
        analogWrite(motorLfront, speed);
        analogWrite(motorRfront, speed);
    }
    /* Can’t see line, Search line */
    else if (dir == 'D')
    {
        // 제자리에서 길을 탐색하기 위해 왼쪽으로 돌면서 길을 탐색
        analogWrite(motorLback, speed);
        analogWrite(motorRfront, speed);
    }
    // 0.01초간 해당 방향으로 주행
    delay(10);
}

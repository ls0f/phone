#include<stdio.h>
#include<string.h>


int swap_int32( int val )
{
	    val = ((val << 8) & 0xFF00FF00) | ((val >> 8) & 0xFF00FF ); 
		    return (val << 16) | ((val >> 16) & 0xFFFF);
}

struct Head{
	char version[4];
	unsigned  int firstRecordOffset;
}head;


struct Phone{
	int phoneNo;
	int offeset;
	unsigned  char type;
}phone;

char * getPhoneInfo(int phoneNo,char * result){
	FILE * fp = fopen("phone.dat","rb");
	if (!fp){
		printf("open phone.dat fail");
		return result;
	}
	fread(&head,sizeof(head),1,fp);
	//printf("%s,%i\n",head.version, head.firstRecordOffset);
	// sizeof(phone) != 9........
	int singerlRecordLength = sizeof(phone.phoneNo) + sizeof(phone.offeset) + sizeof(char);
	//singerlRecordLength = sizeof(phone);
	fseek(fp,0,SEEK_END);
	int recordNum = (ftell(fp) - head.firstRecordOffset)/singerlRecordLength;
	//printf("%i\n",recordNum);
	int l = 0;
	int r = recordNum;
	int m = 0;
	int currentOffset = 0;
	while(l<=r){
		fseek(fp,0,SEEK_SET);
		m = (l+r)/2;
		currentOffset = head.firstRecordOffset+m*singerlRecordLength;	
		fseek(fp,currentOffset,SEEK_SET);
		fread(&phone,singerlRecordLength,1,fp); 
		//printf("%i,%i,%i\n",l,r,phone.phoneNo);
		
		if (phone.phoneNo > phoneNo){
			r = m - 1;
		}
		else if( phone.phoneNo < phoneNo){
			l = m + 1;
		}
		else{
			fseek(fp,0,SEEK_SET);
			fseek(fp,(phone.offeset+sizeof(head)),1);
			int i = 0;
			char ch;
			while(fread(&ch,sizeof(char),1,fp) ){
				if (ch == '\0')
					break;
				result[i++] = ch;
			}
			result[i] = '|';
			char *p = NULL;
			if (phone.type == 1)
				p = "移动";
			else if (phone.type == 2)
				p = "联通";
			else
				p = "电信";
			strcat(result,p);
			break;
		}
	}

	fclose(fp);
	return result;
}


int main(){
	char result[200] = {};
	printf("%s\n",getPhoneInfo(1521147,result));
	return 0;
}

